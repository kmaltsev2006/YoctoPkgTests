import pytest
import allure
import pytest_check as check
from cyp_test_lib.ssh_client import SshClient


@allure.suite('liblsan-staticdev tests')
@pytest.mark.smoke
@pytest.mark.liblsan_staticdev
class TestLibLsanStaticDev:
    '''Tests covering liblsan-staticdev package.'''

    @allure.title('liblsan-staticdev: minimal test')
    @pytest.mark.minimal
    def test_liblsan_static_utilities(self, ssh_client: SshClient):
        """Minimal test: checks if liblsan.a is found by gcc"""
        with allure.step('Check for liblsan.a via gcc'):
            cmd = ssh_client.exec('gcc -print-file-name=liblsan.a', ignore_rc=True)
            assert cmd.rc == 0 and '/' in cmd.stdout.strip() and 'liblsan' in cmd.stdout, \
                f"Liblsan Static failed (Static library liblsan.a not found via gcc search path): out='{cmd.stdout}', err='{cmd.stderr}'"

    # pylint: disable=unused-argument
    @allure.title('liblsan-staticdev: static link and leak detection')
    @pytest.mark.parametrize('are_utils_available', [['g++', 'ldd']], indirect=True)
    def test_liblsan_static_detection(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str, are_utils_available: None):
        """
        Compiles statically with -fsanitize=leak.
        Verifies binary is static and LSan still works.
        """
        source_path = f'{remote_tmp_path}/test_liblsan_static.c'
        binary_path = f'{remote_tmp_path}/test_leak_bin'

        ssh_client.put_file(
            f'{test_files_path}/test_liblsan_static.c', remote_tmp_path)

        with allure.step('Compile statically with -fsanitize=leak'):
            # -static force static linking, -g for debug symbols (optional but good for sanitizers)
            cmd = ssh_client.exec(
                f'gcc -fsanitize=leak {source_path} -o {binary_path} -static-liblsan -static-libgcc -rdynamic -lpthread -ldl -g', ignore_rc=True)
            check.equal(cmd.rc, 0, f"Liblsan Static failed (Compilation failed): out='{cmd.stdout}', err='{cmd.stderr}'")

        with allure.step('Verify liblsan is not linked dynamicaly'):
            cmd = ssh_client.exec(f'! ldd {binary_path} | grep liblsan ', ignore_rc=True)
            check.equal(cmd.rc, 0,
                        f"Liblsan Static failed (liblsan.so found): out='{cmd.stdout}', err='{cmd.stderr}'")

        with allure.step('Verify __lsan_init is in binary'):
            cmd = ssh_client.exec(f'nm {binary_path} | grep __lsan_init', ignore_rc=True)
            check.is_in('T __lsan_init', cmd.stdout,
                        f"Liblsan Static failed (No init in binary): out='{cmd.stdout}', err='{cmd.stderr}'")

        with allure.step('Run static binary and check for leak detection'):
            # LSAN_OPTIONS=exitcode=23 sets a custom exit code when a leak is detected
            cmd = ssh_client.exec(f'LSAN_OPTIONS=exitcode=23 {binary_path}', ignore_rc=True)

            check.equal(cmd.rc, 23, f"Liblsan Static failed (Leak not detected or wrong exit code): out='{cmd.stdout}', err='{cmd.stderr}'")

            check.is_in('LeakSanitizer: detected memory leaks', cmd.stdout + cmd.stderr,
                        f"Liblsan Static failed (Sanitizer report missing): out='{cmd.stdout}', err='{cmd.stderr}'")

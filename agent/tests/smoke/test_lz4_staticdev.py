import pytest
import allure
import pytest_check as check
from cyp_test_lib.ssh_client import SshClient
from helpers import check_static_lib


@allure.suite('lz4-staticdev tests')
@pytest.mark.smoke
@pytest.mark.lz4_staticdev
class TestLz4StaticDev:
    '''Tests covering lz4-staticdev package.'''

    @allure.title('lz4-staticdev: check static libraries')
    @pytest.mark.minimal
    @pytest.mark.parametrize('lib',
                             [
                                 'liblz4.a'
                             ])
    def test_lz4_staticdev_static_libraries(self, lib: str, ssh_client: SshClient):
        '''Testing lz4 static libraries'''
        with allure.step(f'Check {lib}'):
            is_static_lib, msg = check_static_lib(
                ssh_client, f'/usr/lib/{lib}')
            assert is_static_lib, msg

    # pylint: disable=unused-argument
    @allure.title('lz4-staticdev: compile and run (static linkage)')
    @pytest.mark.parametrize('are_utils_available', [['gcc']], indirect=True)
    def test_lz4_staticdev_compilation(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str, are_utils_available):
        '''
        Main test: Verifies static compilation against lz4.
        '''
        source_path = f'{remote_tmp_path}/test_lz4.c'
        binary_path = f'{remote_tmp_path}/test_lz4_static'

        ssh_client.put_file(
            f'{test_files_path}/test_lz4.c', remote_tmp_path)

        with allure.step('Compile statically'):
            # Using -static flag to force static linkage and -llz4
            cmd = ssh_client.exec(
                f'gcc {source_path} -o {binary_path} -static -llz4', ignore_rc=True)
            check.equal(cmd.rc, 0, f"Lz4-staticdev failed (Compilation failed): out='{cmd.stdout}', err='{cmd.stderr}'")

        with allure.step('Run the static binary'):
            cmd = ssh_client.exec(binary_path, ignore_rc=True)
            check.equal(cmd.rc, 0, f"Lz4-staticdev failed (Execution failed): out='{cmd.stdout}', err='{cmd.stderr}'")
            check.is_in('LZ4 Version:', cmd.stdout,
                        f"Lz4-staticdev failed (Output verification failed): out='{cmd.stdout}', err='{cmd.stderr}'")

        with allure.step('Verify binary is static using ldd'):
            cmd = ssh_client.exec(f'ldd {binary_path}', ignore_rc=True)
            is_static = 'not a dynamic executable' in (cmd.stdout + cmd.stderr) or cmd.rc != 0
            check.is_true(is_static, f"Lz4-staticdev failed (Binary is not static): out='{cmd.stdout}', err='{cmd.stderr}'")

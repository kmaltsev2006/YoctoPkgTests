import pytest
import allure
import pytest_check as check
from cyp_test_lib.ssh_client import SshClient


@allure.suite('dwz tests')
@pytest.mark.smoke
@pytest.mark.dwz
class TestDwz:
    '''Tests for the dwz (DWARF squeezing utility) package'''

    @allure.title('dwz: minimal test')
    @pytest.mark.minimal
    def test_dwz_utilities(self, ssh_client: SshClient):
        '''Tests minimal setup of dwz'''
        with allure.step('Check installation'):
            cmd = ssh_client.exec('dwz --version', ignore_rc=True)
            assert cmd.rc == 0, 'dwz is not installed or not in PATH'

    # pylint: disable=unused-argument
    @allure.title('dwz: compress debug info and verify size reduction')
    @pytest.mark.parametrize('are_utils_available', [['g++', 'readelf', 'stat']], indirect=True)
    def test_dwz_shrinks_debug_info(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str, are_utils_available: None):
        '''
        Tests that `dwz` successfully runs on an executable, reduces its size,
        and preserves the essential debug sections.
        '''
        ssh_client.put_file(
            f'{test_files_path}/test_dwz.cpp', remote_tmp_path)

        binary_path = f'{remote_tmp_path}/hello_dwz_debug'

        with allure.step(f'Compiling source file with debug info to {binary_path}'):
            compile_cmd = f'g++ -g -o {binary_path} {remote_tmp_path}/test_dwz.cpp'
            cmd = ssh_client.exec(compile_cmd, ignore_rc=True)
            check.equal(
                cmd.rc, 0,
                f"dwz failed (Compilation failed): out='{cmd.stdout}', err='{cmd.stderr}")


        initial_size = 0
        with allure.step('Get initial file size and check for debug sections'):
            cmd = ssh_client.exec(f"readelf -S {binary_path}", ignore_rc=True)
            check.is_in('.debug_info', cmd.stdout,
                        f"dwz failed ('.debug_info' section not found before running dwz.): out='{cmd.stdout}', err='{cmd.stderr}")

            cmd = ssh_client.exec(f'stat -c %s {binary_path}', ignore_rc=True)
            check.equal(cmd.rc, 0,
                        f"dwz failed (Failed to get initial file size): out='{cmd.stdout}', err='{cmd.stderr}")

            initial_size = int(cmd.stdout.strip())

        with allure.step(f'Run dwz on the binary file: {binary_path}'):
            cmd = ssh_client.exec(f'dwz {binary_path}', ignore_rc=True)
            check.equal(
                cmd.rc, 0,
                f"dwz failed (dwz execution failed): out='{cmd.stdout}', err='{cmd.stderr}")

        final_size = 0
        with allure.step('Get final file size and re-check for debug sections'):
            cmd = ssh_client.exec(f'readelf -S {binary_path}', ignore_rc=True)
            check.is_in('.debug_info', cmd.stdout,
                        f"dwz failed ('.debug_info' section disappeared after running dwz): out='{cmd.stdout}', err='{cmd.stderr}")

            cmd = ssh_client.exec(f'stat -c %s {binary_path}', ignore_rc=True)
            check.equal(cmd.rc, 0,
                        f"dwz failed (Failed to get final file size.): out='{cmd.stdout}', err='{cmd.stderr}")
            final_size = int(cmd.stdout.strip())

        with allure.step('Verify that the file size has decreased'):
            check.is_true(final_size > 0,
                          f"dwz failed (Final file size is zero): out='{cmd.stdout}', err='{cmd.stderr}")
            check.is_true(final_size < initial_size,
                          f"dwz failed (File size did not decrease after running dwz "
                          f"Initial: {initial_size}, Final: {final_size}'): out='{cmd.stdout}', err='{cmd.stderr}")

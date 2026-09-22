import pytest
import allure
import pytest_check as check
from cyp_test_lib.ssh_client import SshClient


@allure.suite('cpp tests')
@pytest.mark.smoke
@pytest.mark.cpp
class TestCpp:
    '''cpp smoke test class'''
    @allure.title('cpp: version test')
    @pytest.mark.minimal
    def test_cpp_version(self, ssh_client: SshClient):
        '''Test cpp installed version'''
        with allure.step('Checking installed version'):
            cmd = ssh_client.exec('cpp --version', ignore_rc=True)
            assert cmd.rc == 0, f"cpp failed (not installed): out='{cmd.stdout}', err='{cmd.stderr}'"

    @allure.title('cpp: basic preprocessing')
    @pytest.mark.minimal
    def test_cpp(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str):
        '''Test cpp basic functionality'''
        ssh_client.put_file(
            f'{test_files_path}/test_cpp.c', remote_tmp_path)
        with allure.step('Checking cpp preprocessing'):
            cmd = ssh_client.exec(
                f'cpp {remote_tmp_path}/test_cpp.c', ignore_rc=True)
            check.equal(
                cmd.rc, 0, f"cpp failed: out='{cmd.stdout}', err='{cmd.stderr}'")
            # has to be in preprocessed code
            occurrences = ['test_cpp.c', '/usr/include', 'int c = 5 + 8;']
            for occurrence in occurrences:
                check.is_in(occurrence, cmd.stdout,
                            f"cpp failed (expected '{occurrence}' in stdout): out='{cmd.stdout}', err='{cmd.stderr}'")

import pytest
import allure
from cyp_test_lib.ssh_client import SshClient
from helpers import check_elf_file


@allure.suite('acl-dev tests')
@pytest.mark.smoke
@pytest.mark.acl_dev
class TestAclDev:
    '''acl-dev smoke test class'''

    @allure.title('acl-dev: headers test')
    @pytest.mark.minimal
    def test_acl_dev_headers(self, ssh_client: SshClient):
        '''Test acl-dev headers installed'''
        with allure.step('Checking acl-dev headers'):
            cmd = ssh_client.exec(
                'stat /usr/include/sys/acl.h', ignore_rc=True)
            assert cmd.rc == 0, f"acl-dev failed (headers not found): out='{cmd.stdout}', err='{cmd.stderr}'"

    @allure.title('acl-dev: libraries test')
    @pytest.mark.minimal
    def test_acl_dev_lib(self, ssh_client: SshClient):
        '''Test acl-dev libraries installed'''
        with allure.step('Checking acl-dev libraries'):
            is_elf, msg = check_elf_file(ssh_client, '/usr/lib/libacl.so')
            assert is_elf, f'acl-dev failed: {msg}'

    @allure.title('acl-dev: compile and link test')
    def test_acl_dev(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str):
        '''Testing linkage with lacl and usage basic acl type'''
        ssh_client.put_file(
            f'{test_files_path}/test_acldev.c', remote_tmp_path)
        with allure.step('Testing program compilation and run'):
            command = f'gcc {remote_tmp_path}/test_acldev.c -o {remote_tmp_path}/test_acldev -lacl && {remote_tmp_path}/test_acldev'
            cmd = ssh_client.exec(command, ignore_rc=True)
            assert cmd.rc == 0 and 'ACL_FUNCTIONS_WORK' in cmd.stdout and 'FAILED' not in cmd.stdout, f"acl-dev failed:\
                  out='{cmd.stdout}', err='{cmd.stderr}'"

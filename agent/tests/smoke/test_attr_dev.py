import pytest
import allure
from cyp_test_lib.ssh_client import SshClient
from helpers import check_elf_file


@allure.suite('attr-dev tests')
@pytest.mark.smoke
@pytest.mark.attr_dev
class TestAttrDev:
    '''attr-dev smoke test class'''

    @allure.title('attr-dev: headers test')
    @pytest.mark.minimal
    def test_attr_dev_headers(self, ssh_client: SshClient):
        '''Test attr-dev installed headers'''
        with allure.step('Checking headers installed'):
            cmd = ssh_client.exec(
                'stat /usr/include/attr/attributes.h', ignore_rc=True)
            assert cmd.rc == 0, f"attr-dev failed (headers not found): out='{cmd.stdout}', err='{cmd.stderr}'"

    @allure.title('attr-dev: libraries test')
    @pytest.mark.minimal
    def test_attr_dev_lib(self, ssh_client: SshClient):
        '''Test attr-dev libraries installed'''
        with allure.step('Checking attr-dev libraries'):
            is_elf, msg = check_elf_file(ssh_client, '/usr/lib/libattr.so')
            assert is_elf, f'attr-dev failed: {msg}'

    @allure.title('attr-dev: compile, link and run test')
    def test_attr_dev(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str):
        '''Testing linkage and runtime usage'''
        ssh_client.put_file(
            f'{test_files_path}/test_attrdev.c', remote_tmp_path)
        with allure.step('Checking program compilation and run'):
            command = f'gcc {remote_tmp_path}/test_attrdev.c -o {remote_tmp_path}/test_attrdev -lattr && {remote_tmp_path}/test_attrdev'
            cmd = ssh_client.exec(command, ignore_rc=True)
            assert cmd.rc == 0 and 'LIBATTR_WORKS' in cmd.stdout and 'FAILED' not in cmd.stdout, f"attr-dev failed:\
                  out='{cmd.stdout}', err='{cmd.stderr}'"

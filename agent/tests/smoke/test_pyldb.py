import pytest
import allure
import pytest_check as check
from cyp_test_lib.ssh_client import SshClient
from helpers import check_elf_file


@allure.suite('pyldb tests')
@pytest.mark.smoke
@pytest.mark.pyldb
class TestPyldb:
    '''pyldb smoke test class'''

    @allure.title('pyldb: Python module import test')
    @pytest.mark.minimal
    def test_pyldb_module_so(self, ssh_client: SshClient):
        '''Test pyldb Python module can be imported'''
        with allure.step('Checking libldb.so'):
            is_elf, msg = check_elf_file(ssh_client, '/usr/lib/libldb.so')
            assert is_elf, f'pyldb failed: {msg}'

    @allure.title('pyldb: module functionality test')
    def test_pyldb_functionality(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str):
        '''Test basic pyldb module functionality'''
        ssh_client.put_file(
            f'{test_files_path}/pyldb.py', remote_tmp_path)
        with allure.step('Testing ldb module basic functions'):
            cmd = ssh_client.exec(
               f'python3 {remote_tmp_path}/pyldb.py', ignore_rc=True)
            check.equal(
                cmd.rc, 0, f"pyldb failed (module not functional): out='{cmd.stdout}', err='{cmd.stderr}'")
            check.is_in('LDB_MODULE_IMPORTED', cmd.stdout,
                        f"pyldb failed (module not functional): out='{cmd.stdout}, err='{cmd.stderr}'")
            check.is_in('LDB_CONTEXT_CREATED', cmd.stdout,
                        f"pyldb failed (module not functional): out='{cmd.stdout}, err='{cmd.stderr}'")

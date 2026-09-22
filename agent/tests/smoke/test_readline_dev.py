import pytest
import allure
from cyp_test_lib.ssh_client import SshClient
from helpers import check_elf_file

@allure.suite('readline-dev tests')
@pytest.mark.smoke
@pytest.mark.readline_dev
class TestReadlineDev:
    '''readline-dev smoke test class'''

    @allure.title('readline-dev: check headers')
    @pytest.mark.minimal
    @pytest.mark.parametrize('header', [
        '/usr/include/readline/readline.h',
        '/usr/include/readline/history.h'
    ])
    def test_readline_dev_headers(self, ssh_client: SshClient, header: str):
        with allure.step(f'Check {header}'):
            cmd = ssh_client.exec(f'test -e {header}', ignore_rc=True)
            assert cmd.rc == 0, f'Header not found: {header}'

    @allure.title('readline-dev: check shared libraries')
    @pytest.mark.minimal
    def test_readline_dev_shared_lib(self, ssh_client: SshClient):
        with allure.step('Check libreadline.so'):
            is_elf, msg = check_elf_file(ssh_client, '/usr/lib/libreadline.so')
            assert is_elf, msg

    # pylint: disable=unused-argument
    @allure.title('readline-dev: check workability')
    @pytest.mark.minimal
    @pytest.mark.parametrize('are_utils_available', [['gcc']], indirect=True)
    def test_readline_dev_workability(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str, are_utils_available: None):
        ssh_client.put_file(f'{test_files_path}/test_readline.c', remote_tmp_path)

        with allure.step('Compile and run'):
            cmd = ssh_client.exec(
                f'gcc -o {remote_tmp_path}/a.out {remote_tmp_path}/test_readline.c -lreadline -lhistory &&\
{remote_tmp_path}/a.out', ignore_rc=True)
            assert cmd.rc == 0, f'readline-dev is broken: {cmd.stderr}'

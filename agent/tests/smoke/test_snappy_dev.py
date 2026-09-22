import pytest
import allure
from cyp_test_lib.ssh_client import SshClient
from helpers import check_elf_file

@allure.suite('snappy-dev tests')
@pytest.mark.smoke
@pytest.mark.snappy_dev
class TestSnappyDev:
    '''snappy-dev smoke test class'''

    @allure.title('snappy-dev: check headers')
    @pytest.mark.minimal
    def test_snappy_dev_headers(self, ssh_client: SshClient):
        with allure.step('Check snappy.h'):
            cmd = ssh_client.exec('test -e /usr/include/snappy.h', ignore_rc=True)
            assert cmd.rc == 0, f'Header not found: {cmd.stderr}'

    @allure.title('snappy-dev: check shared libraries')
    @pytest.mark.minimal
    def test_snappy_dev_shared_libraries(self, ssh_client: SshClient):
        with allure.step('Check libsnappy.so'):
            is_elf, msg = check_elf_file(ssh_client, '/usr/lib/libsnappy.so')
            assert is_elf, msg

    # pylint: disable=unused-argument
    @allure.title('snappy-dev: check workability')
    @pytest.mark.minimal
    @pytest.mark.parametrize('are_utils_available', [['g++']], indirect=True)
    def test_snappy_dev_workability(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str, are_utils_available: None):
        ssh_client.put_file(f'{test_files_path}/test_snappy_dev.cpp', remote_tmp_path)

        with allure.step('Compile and run'):
            cmd = ssh_client.exec(f'g++ -o {remote_tmp_path}/a.out {remote_tmp_path}/test_snappy_dev.cpp -lsnappy &&\
{remote_tmp_path}/a.out', ignore_rc=True)
            assert cmd.rc == 0, f'snappy-dev is broken: {cmd.stderr}'

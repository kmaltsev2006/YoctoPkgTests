import pytest
import allure
from cyp_test_lib.ssh_client import SshClient
from helpers import check_elf_file


@allure.suite('zeromq-dev tests')
@pytest.mark.smoke
@pytest.mark.zeromq_dev
class TestZeroMqDev:
    '''zeromq-dev smoke test class'''

    @allure.title('zeromq-dev: check headers')
    @pytest.mark.minimal
    def test_zeromq_dev_headers(self, ssh_client: SshClient):
        '''Testing zeromq headers installed'''
        with allure.step('Check zmq.h presence'):
            cmd = ssh_client.exec('test -f /usr/include/zmq.h', ignore_rc=True)
            assert cmd.rc == 0, f"zeromq-dev failed (headers not found) out='{cmd.stdout}', err='{cmd.stderr}'"

    @allure.title('zeromq-dev: check shared libraries')
    @pytest.mark.minimal
    @pytest.mark.parametrize('lib', ['libzmq.so'])
    def test_zeromq_dev_shared_libraries(self, lib: str, ssh_client: SshClient):
        '''Testing zeromq shared libraries installed'''
        with allure.step(f'Check {lib}'):
            is_elf, msg = check_elf_file(ssh_client, f'/usr/lib/{lib}')
            assert is_elf, f"zeromq-dev failed (shared library {lib} check failed) out='{msg}', err=''"

    # pylint: disable=unused-argument
    @allure.title('zeromq-dev: check workability')
    @pytest.mark.parametrize('are_utils_available', [['g++']], indirect=True)
    def test_zeromq_dev_workability(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str, are_utils_available: None):
        '''Testing zeromq basic workability via compilation'''
        ssh_client.put_file(f'{test_files_path}/test_zeromq_dev.cpp', remote_tmp_path)

        with allure.step('Compile and run'):
            cmd = ssh_client.exec(
                f'g++ -o {remote_tmp_path}/zmq_test {remote_tmp_path}/test_zeromq_dev.cpp -lzmq && {remote_tmp_path}/zmq_test',
                ignore_rc=True
            )
            assert cmd.rc == 0, f"zeromq-dev failed (compilation or execution failed) out='{cmd.stdout}', err='{cmd.stderr}'"

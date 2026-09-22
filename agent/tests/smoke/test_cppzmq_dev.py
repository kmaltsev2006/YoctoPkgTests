import pytest
import allure
from cyp_test_lib.ssh_client import SshClient


@allure.suite('cppzmq-dev tests')
@pytest.mark.smoke
@pytest.mark.cppzmq_dev
class TestCppZmqDev:
    '''cppzmq-dev smoke test'''

    @allure.title('cppzmq-dev: header exists')
    @pytest.mark.minimal
    def test_header_exists(self, ssh_client: SshClient):
        '''Testing headers'''
        with allure.step('Verifying presence of /usr/include/zmq.hpp header'):
            cmd = ssh_client.exec('test -f /usr/include/zmq.hpp', ignore_rc=True)
            assert cmd.rc == 0, cmd.stderr

    # pylint: disable=unused-argument
    @allure.title('cppzmq-dev: compile minimal program')
    @pytest.mark.parametrize('are_utils_available', [['c++']], indirect=True)
    def test_compile_minimal_cppzmq(
        self,
        ssh_client: SshClient,
        test_files_path: str,
        remote_tmp_path: str,
        are_utils_available: None
    ):
        '''Compile and run a minimal C++ program'''
        with allure.step('Copy minimal C++ program to target'):
            ssh_client.put_file(
                f'{test_files_path}/test_cppzmq_dev.cpp',
                f'{remote_tmp_path}/test_cppzmq_dev.cpp'
            )

        with allure.step('Compiling and running the C++ program with -lzmq'):
            cmd = ssh_client.exec(
                f'c++ {remote_tmp_path}/test_cppzmq_dev.cpp -o {remote_tmp_path}/test_cppzmq -lzmq && {remote_tmp_path}/test_cppzmq',
                ignore_rc=True
            )
            assert cmd.rc == 0, cmd.stderr

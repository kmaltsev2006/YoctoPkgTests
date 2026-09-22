import pytest
import allure
from cyp_test_lib.ssh_client import SshClient

@allure.suite('libevent-dev tests')
@pytest.mark.smoke
@pytest.mark.libevent_dev
class TestLibeventDev:
    '''libevent-dev smoke test class'''

    @allure.title('libevent-dev: headers test')
    @pytest.mark.minimal
    def test_libevent_dev_headers(self, ssh_client: SshClient) -> None:
        '''Test libevent-dev installed headers'''
        with allure.step('Check if event.h exists'):
            cmd = ssh_client.exec('stat /usr/include/event2/event.h', ignore_rc=True)
            assert cmd.rc == 0, f'libevent headers not found: {cmd.stderr}'

    @allure.title('libevent-dev: compile test')
    @pytest.mark.require_packages(['gcc'])
    def test_libevent_dev_compile(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str) -> None:
        '''Test libevent-dev compilation'''

        with allure.step('Upload test source file'):
            ssh_client.put_file(
                f'{test_files_path}/test_event.c', remote_tmp_path)

        with allure.step('Compile and run'):
            command = f"gcc {remote_tmp_path}/test_event.c -o {remote_tmp_path}/test_libevent -levent && \
                {remote_tmp_path}/test_libevent"
            cmd = ssh_client.exec(command)
            assert cmd.rc == 0, f'libevent-dev compilation failed: {cmd.stderr}'
            assert 'LIBEVENT_INITIALIZED' in cmd.stdout

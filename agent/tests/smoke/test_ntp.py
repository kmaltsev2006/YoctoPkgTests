import pytest
import allure
from cyp_test_lib.ssh_client import SshClient


@allure.suite('ntp tests')
@pytest.mark.smoke
@pytest.mark.ntp
class TestNtp:
    '''ntp smoke test class'''

    @allure.title('ntp: check installation')
    @pytest.mark.minimal
    def test_ntp_installation(self, ssh_client: SshClient):
        with allure.step('Check ntp installation'):
            cmd = ssh_client.exec('which ntpq', ignore_rc=True)
            assert cmd.rc == 0, f'{cmd.stderr}'

    @allure.title('ntp: check workability')
    @pytest.mark.minimal
    def test_ntp_workability(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str):
        '''Test ntp command functionality'''
        with allure.step('Copy test_ntp.conf to target'):
            ssh_client.put_file(
                f'{test_files_path}/test_ntp.conf', remote_tmp_path)
        with allure.step('Check ntpq workability'):
            cmd = ssh_client.exec(f'ntpq -c "readvar {remote_tmp_path}/test_ntp.conf"', ignore_rc=True)
            assert cmd.rc == 0, f'ntp is broken: {cmd.stderr}'

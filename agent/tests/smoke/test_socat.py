import pytest
import allure
from cyp_test_lib.ssh_client import SshClient

@allure.suite('socat tests')
@pytest.mark.smoke
@pytest.mark.socat
class TestSocat:
    '''socat smoke test class'''

    @allure.title('socat: check installation')
    @pytest.mark.minimal
    def test_socat_installation(self, ssh_client: SshClient):
        '''Check if socat utility is installed'''
        with allure.step('Check socat installation'):
            cmd = ssh_client.exec('which socat', ignore_rc=True)
            assert cmd.rc == 0, f'socat not found: {cmd.stderr}'

    @allure.title('socat: check workability')
    @pytest.mark.minimal
    def test_socat_workability(self, ssh_client: SshClient, remote_tmp_path: str):
        '''Test socat data transfer between files'''
        input_file = f'{remote_tmp_path}/test_socat.in'
        output_file = f'{remote_tmp_path}/test_socat.out'
        test_data = 'socat_test_datas'

        with allure.step('Prepare test data'):
            ssh_client.exec(f'echo "{test_data}" > {input_file}')

        with allure.step('Run socat file-to-file transfer'):
            # Copy content from one file to another using socat
            cmd = ssh_client.exec(f'socat GOPEN:{input_file} GOPEN:{output_file}', ignore_rc=True)
            assert cmd.rc == 0, f'socat transfer failed: {cmd.stderr}'

        with allure.step('Verify transferred data'):
            cmd_check = ssh_client.exec(f'cat {output_file}', ignore_rc=True)
            assert test_data in cmd_check.stdout, f'Data mismatch: {cmd_check.stdout}'

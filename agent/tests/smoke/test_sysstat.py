import pytest
import allure
import pytest_check as check
from cyp_test_lib.ssh_client import SshClient


@allure.suite('sysstat tests')
@pytest.mark.smoke
@pytest.mark.sysstat
class TestSysstat:
    '''sysstat smoke test class'''

    @allure.title('sysstat: check installation')
    @pytest.mark.minimal
    @pytest.mark.parametrize('utility', [
        'sar',
        'sadf',
        'iostat',
        'mpstat',
        'pidstat',
        'tapestat',
        'cifsiostat'
    ])
    def test_sysstat_installation(self, ssh_client: SshClient, utility: str):
        '''Check installed utilities via which'''
        with allure.step(f'Check {utility} installation'):
            cmd = ssh_client.exec(f'which {utility}', ignore_rc=True)
            assert cmd.rc == 0, f'sysstat failed ({utility} not found) out="{cmd.stdout}", err="{cmd.stderr}"'

    @allure.title('iostat: check workability')
    @pytest.mark.minimal
    def test_sysstat_iostat_workability(self, ssh_client: SshClient):
        '''Test iostat basic functionality'''
        with allure.step('Check iostat output'):
            cmd = ssh_client.exec('iostat -x 1 1', ignore_rc=True)
            assert cmd.rc == 0, f'sysstat failed (iostat execution error) out="{cmd.stdout}", err="{cmd.stderr}"'

    @allure.title('mpstat: check workability')
    @pytest.mark.minimal
    def test_sysstat_mpstat_workability(self, ssh_client: SshClient):
        '''Test mpstat basic functionality'''
        with allure.step('Check mpstat output'):
            cmd = ssh_client.exec('mpstat -P ALL 1 1', ignore_rc=True)
            assert cmd.rc == 0, f'sysstat failed (mpstat execution error) out="{cmd.stdout}", err="{cmd.stderr}"'

    @allure.title('pidstat: check workability')
    def test_sysstat_pidstat_workability(self, ssh_client: SshClient):
        '''Test pidstat functionality'''
        with allure.step('Check pidstat monitoring'):
            cmd = ssh_client.exec('pidstat -u 1 1', ignore_rc=True)
            assert cmd.rc == 0, f'sysstat failed (pidstat execution error) out="{cmd.stdout}", err="{cmd.stderr}"'

    @allure.title('sar: check workability')
    def test_sysstat_sar_workability(self, ssh_client: SshClient, remote_tmp_path: str):
        '''Test sar functionality with data collection and reading'''
        with allure.step('Collect data to file'):
            collect_cmd = ssh_client.exec(f'sar -o {remote_tmp_path}/test_sysstat.data 1 1', ignore_rc=True)
            assert collect_cmd.rc == 0, f'sysstat failed (sar collection error) out="{collect_cmd.stdout}", err="{collect_cmd.stderr}"'

        with allure.step('Read collected data'):
            read_cmd = ssh_client.exec(f'sar -f {remote_tmp_path}/test_sysstat.data', ignore_rc=True)
            assert read_cmd.rc == 0, f'sysstat failed (sar reading error) out="{read_cmd.stdout}", err="{read_cmd.stderr}"'

    @allure.title('sadf: check data conversion')
    def test_sysstat_sadf_workability(self, ssh_client: SshClient, remote_tmp_path: str):
        '''Test sadf data conversion functionality'''
        with allure.step('Generate data and convert to CSV'):
            cmd = ssh_client.exec(f'sar -o {remote_tmp_path}/test_sysstat.sadf 1 1 && sadf -d {remote_tmp_path}/test_sysstat.sadf', ignore_rc=True)
            check.equal(cmd.rc, 0, f'sysstat failed (sadf conversion error) out="{cmd.stdout}", err="{cmd.stderr}"')
            check.is_not_none(cmd.stdout, f'sysstat failed (sadf output is empty) out="{cmd.stdout}", err="{cmd.stderr}"')

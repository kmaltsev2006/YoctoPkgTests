import pytest
import allure
import pytest_check as check
from cyp_test_lib.ssh_client import SshClient


@allure.suite('util-linux tests')
@pytest.mark.smoke
@pytest.mark.util_linux
class TestUtilLinux:
    '''util-linux smoke test class'''

    @allure.title('util-linux: check installation')
    @pytest.mark.minimal
    @pytest.mark.parametrize('utility', [
        'fdisk',
        'lsblk',
        'mount',
        'umount',
        'dmesg',
        'findmnt',
        'kill',
        'more'
    ])
    def test_util_linux_installation(self, ssh_client: SshClient, utility: str):
        '''Check installed utilities via which'''
        with allure.step(f'Check {utility} installation'):
            cmd = ssh_client.exec(f'which {utility}', ignore_rc=True)
            assert cmd.rc == 0, f"util-linux failed ({utility} not found) out='{cmd.stdout}', err='{cmd.stderr}'"

    @allure.title('lsblk: check workability')
    @pytest.mark.minimal
    def test_util_linux_lsblk_workability(self, ssh_client: SshClient):
        '''Test lsblk basic functionality'''
        with allure.step('Check lsblk output'):
            cmd = ssh_client.exec('lsblk -o NAME,SIZE', ignore_rc=True)
            assert cmd.rc == 0, f"util-linux failed (lsblk execution error) out='{cmd.stdout}', err='{cmd.stderr}'"

    @allure.title('findmnt: check workability')
    def test_util_linux_findmnt_workability(self, ssh_client: SshClient):
        '''Test findmnt functionality'''
        with allure.step('Check findmnt on root filesystem'):
            cmd = ssh_client.exec('findmnt /', ignore_rc=True)
            assert cmd.rc == 0, f"util-linux failed (findmnt execution error) out='{cmd.stdout}', err='{cmd.stderr}'"
            assert '/' in cmd.stdout, f"util-linux failed (invalid findmnt output) out='{cmd.stdout}', err='{cmd.stderr}'"

    @allure.title('fdisk: check readonly list')
    def test_util_linux_fdisk_list(self, ssh_client: SshClient):
        '''Test fdisk list functionality using sudo'''
        with allure.step('Check fdisk -l with sudo'):
            cmd = ssh_client.exec_sudo('fdisk -l', ignore_rc=True)
            assert cmd.rc == 0, f"util-linux failed (fdisk -l execution failed) out='{cmd.stdout}', err='{cmd.stderr}'"

    @allure.title('cal: check output')
    def test_util_linux_cal_workability(self, ssh_client: SshClient):
        '''Test cal utility functionality'''
        with allure.step('Check calendar for 2026'):
            cmd = ssh_client.exec('cal 2026', ignore_rc=True)
            check.equal(cmd.rc, 0, f"util-linux failed (cal execution error) out='{cmd.stdout}', err='{cmd.stderr}'")
            check.is_in('2026', cmd.stdout, f"util-linux failed (cal output error) out='{cmd.stdout}', err='{cmd.stderr}'")

    @allure.title('lscpu: check cpu info')
    def test_util_linux_lscpu(self, ssh_client: SshClient):
        '''Test lscpu functionality'''
        with allure.step('Check lscpu output'):
            cmd = ssh_client.exec('lscpu', ignore_rc=True)
            assert cmd.rc == 0, f"util-linux failed (lscpu execution error) out='{cmd.stdout}', err='{cmd.stderr}'"
            assert 'CPU(s):' in cmd.stdout, f"util-linux failed (lscpu content error) out='{cmd.stdout}', err='{cmd.stderr}'"

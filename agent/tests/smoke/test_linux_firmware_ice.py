import pytest
import allure
from cyp_test_lib.ssh_client import SshClient


@allure.suite('linux-firmware-ice tests')
@pytest.mark.smoke
@pytest.mark.linux_firmware_ice
class TestLinuxFirmwareIce:
    '''linux-firmware-ice smoke test class'''

    @allure.title('linux-firmware-ice: firmware files test')
    @pytest.mark.minimal
    def test_linux_firmware_ice_files(self, ssh_client: SshClient):
        '''Test ice firmware files installed'''
        with allure.step('Checking ice firmware directory'):
            cmd = ssh_client.exec(
                'ls -d /lib/firmware/updates/intel/ice/ddp/ 2>/dev/null || ls -d /lib/firmware/intel/ice/ddp/ 2>/dev/null',
                ignore_rc=True
            )
            assert cmd.rc == 0, f'ice firmware directory not found: {cmd.stderr}'

    @allure.title('linux-firmware-ice: specific firmware test')
    def test_linux_firmware_ice_specific(self, ssh_client: SshClient):
        '''Test ice specific firmware files'''
        with allure.step('Checking for ice firmware files'):
            cmd = ssh_client.exec(
                'find /lib/firmware -name "*ice*" -type f | head -5',
                ignore_rc=True
            )
            assert cmd.rc == 0 and cmd.stdout.strip(), f'No ice firmware files found: {cmd.stderr}'

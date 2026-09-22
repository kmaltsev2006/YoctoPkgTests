import pytest
import allure
import pytest_check as check
from cyp_test_lib.ssh_client import SshClient


@allure.suite('qemu-common tests')
@pytest.mark.smoke
@pytest.mark.qemu_common
class TestQemuCommon:
    '''Smoke tests for the qemu-common package'''

    @allure.title('qemu-common: minimal installation test')
    @pytest.mark.minimal
    def test_qemu_common_dir(self, ssh_client: SshClient):
        '''Test if qemu shared data directory exists'''
        with allure.step('Checking qemu share directory'):
            cmd = ssh_client.exec('test -d /usr/share/qemu', ignore_rc=True)
            assert cmd.rc == 0, f"qemu-common failed (Shared directory not found): out='{cmd.stdout}', err='{cmd.stderr}'"

    @allure.title('qemu-common: utility version test')
    @pytest.mark.minimal
    def test_qemu_img_version(self, ssh_client: SshClient):
        '''Test qemu-img utility availability'''
        with allure.step('Check qemu-img version'):
            cmd = ssh_client.exec('qemu-img --version', ignore_rc=True)
            assert cmd.rc == 0, f"qemu-common failed (qemu-img not working): out='{cmd.stdout}', err='{cmd.stderr}'"

    # pylint: disable=unused-argument
    @allure.title('qemu-common: functional image creation')
    @pytest.mark.parametrize('are_utils_available', [['qemu-img']], indirect=True)
    def test_qemu_common_functional(self, ssh_client: SshClient, remote_tmp_path: str, are_utils_available: None):
        '''
        Tests basic functional capabilities:
        1. Create a 10MB qcow2 image.
        2. Verify image info.
        '''
        img_path = f'{remote_tmp_path}/test_disk.qcow2'

        with allure.step('Creating qcow2 disk image'):
            cmd = ssh_client.exec(f'qemu-img create -f qcow2 {img_path} 10M', ignore_rc=True)
            check.equal(cmd.rc, 0, f"qemu-common failed (Image creation failed): out='{cmd.stdout}', err='{cmd.stderr}'")

        with allure.step('Verifying image info'):
            cmd = ssh_client.exec(f'qemu-img info {img_path}', ignore_rc=True)
            check.equal(cmd.rc, 0, f"qemu-common failed (Could not read image info): out='{cmd.stdout}', err='{cmd.stderr}'")
            check.is_in('format: qcow2', cmd.stdout,
                        f"qemu-common failed (Incorrect image format): out='{cmd.stdout}', err='{cmd.stderr}'")
            check.is_in('virtual size: 10 MiB', cmd.stdout,
                        f"qemu-common failed (Incorrect image size): out='{cmd.stdout}', err='{cmd.stderr}'")

    @allure.title('qemu-common: firmware existence test')
    @pytest.mark.minimal
    def test_qemu_common_firmware(self, ssh_client: SshClient):
        '''Test if essential firmware/BIOS files are present'''
        with allure.step('Checking for BIOS ROM files'):
            cmd = ssh_client.exec('ls /usr/share/qemu/*.bin /usr/share/qemu/*.rom', ignore_rc=True)
            assert cmd.rc == 0, f"qemu-common failed (Firmware files not found): out='{cmd.stdout}', err='{cmd.stderr}'"

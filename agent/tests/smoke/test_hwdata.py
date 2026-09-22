import pytest
import allure
import pytest_check as check
from cyp_test_lib.ssh_client import SshClient


@allure.suite('hwdata tests')
@pytest.mark.smoke
@pytest.mark.hwdata
class TestHwdata:
    '''Tests for the hwdata package (hardware identification databases)'''
    base_dir = '/usr/share/hwdata'

    @allure.title('hwdata: minimal test')
    @pytest.mark.minimal
    def test_hwdata_utilities(self, ssh_client: SshClient):
        '''Tests minimal setup of hwdata'''
        with allure.step('Check base directory'):
            cmd = ssh_client.exec(f'test -d {self.base_dir}', ignore_rc=True)
            assert cmd.rc == 0, f"Hwdata failed (Base directory {self.base_dir} not found): out='{cmd.stdout}', err='{cmd.stderr}'"

    @allure.title('hwdata: verify USB and PCI IDs database content')
    def test_hwdata_ids(self, ssh_client: SshClient):
        '''
        Verifies that the main directory for hwdata exists.
        Checks for the existence of pci.ids and looks for a known vendor (Intel).
        Checks for the existence of usb.ids and looks for a known vendor (Linux Foundation).
        '''
        with allure.step(f'Check directory existence: {self.base_dir}'):
            cmd = ssh_client.exec(f'test -d {self.base_dir}', ignore_rc=True)
            check.equal(
                cmd.rc, 0, f"Hwdata failed (Directory {self.base_dir} not found): out='{cmd.stdout}', err='{cmd.stderr}'")

        file_path = f'{self.base_dir}/pci.ids'

        with allure.step(f'Check file existence: {file_path}'):
            cmd = ssh_client.exec(f'test -f {file_path}', ignore_rc=True)
            check.equal(cmd.rc, 0, f"Hwdata failed (File {file_path} not found): out='{cmd.stdout}', err='{cmd.stderr}'")

        with allure.step('Verify content (search for Intel Corporation)'):
            cmd = ssh_client.exec(
                f"grep -q 'Intel Corporation' {file_path}", ignore_rc=True)
            check.equal(
                cmd.rc, 0, f"Hwdata failed (Vendor 'Intel Corporation' not found in pci.ids): out='{cmd.stdout}', err='{cmd.stderr}'")

        file_path = f'{self.base_dir}/usb.ids'

        with allure.step(f'Check file existence: {file_path}'):
            cmd = ssh_client.exec(f'test -f {file_path}', ignore_rc=True)
            check.equal(cmd.rc, 0, f"Hwdata failed (File {file_path} not found): out='{cmd.stdout}', err='{cmd.stderr}'")

        with allure.step('Verify content (search for Linux Foundation)'):
            cmd = ssh_client.exec(
                f"grep -q 'Linux Foundation' {file_path}", ignore_rc=True)
            check.equal(
                cmd.rc, 0, f"Hwdata failed (Vendor 'Linux Foundation' not found in usb.ids): out='{cmd.stdout}', err='{cmd.stderr}'")

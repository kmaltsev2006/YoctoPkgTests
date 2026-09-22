import pytest
import allure
from typing import Iterator, Tuple
import pytest_check as check
from cyp_test_lib.ssh_client import SshClient


@allure.suite('dracut tests')
@pytest.mark.smoke
@pytest.mark.dracut
class TestDracut:
    '''Tests for the dracut (initramfs generator) package'''

    @pytest.fixture(scope='function')
    def setup_dracut_env(self, ssh_client: SshClient, remote_tmp_path: str) -> Iterator[Tuple[str, str]]:
        '''
        Fixture to prepare for dracut testing.
        Checks for kernel version and creates image path.
        '''

        cmd = ssh_client.exec('uname -r', ignore_rc=True)
        check.equal(
            cmd.rc, 0, f"Dracut failed (Failed to get kernel version): out='{cmd.stdout}', err='{cmd.stderr}")
        kernel_version = cmd.stdout.strip()

        image_path = f"{remote_tmp_path}/initramfs-{kernel_version}-test.img"

        yield kernel_version, image_path

    @allure.title('dracut: minimal test')
    @pytest.mark.minimal
    def test_dracut_utilities(self, ssh_client: SshClient):
        '''Tests minimal setup of dracut'''
        with allure.step('Check installation'):
            cmd = ssh_client.exec('dracut --version', ignore_rc=True)
            assert cmd.rc == 0, f"Dracut failed (Dracut is not installed): out='{cmd.stdout}', err='{cmd.stderr}"

    # pylint: disable=unused-argument
    @allure.title('dracut: generate initramfs image for current kernel')
    @pytest.mark.parametrize('are_utils_available', [['lsinitrd']], indirect=True)
    def test_dracut_image_generation(self, ssh_client: SshClient, setup_dracut_env, are_utils_available: None):
        '''
        Tests that dracut can successfully generate an initramfs image
        for the currently running kernel, and verifies the image structure.
        '''
        kernel_version, image_path = setup_dracut_env

        with allure.step(f'Generate initramfs for kernel {kernel_version}'):
            command = f"dracut --force {image_path} {kernel_version}"
            cmd = ssh_client.exec(command, ignore_rc=True)
            check.equal(
                cmd.rc, 0,
                f"Dracut failed (Dracut generation failed): out='{cmd.stdout}', err='{cmd.stderr}")

        with allure.step('Verify that image file exists and is not empty'):
            cmd = ssh_client.exec(f'test -s {image_path}', ignore_rc=True)
            check.equal(cmd.rc, 0,
                        f"Dracut failed (Generated image file is missing or empty): out='{cmd.stdout}', err='{cmd.stderr}")

        with allure.step('Inspect image content using lsinitrd'):
            cmd = ssh_client.exec(
                fr"lsinitrd {image_path} | grep -E '\sinit\s'", ignore_rc=True)
            check.equal(
                cmd.rc, 0,
                f"Dracut failed (The 'init' script was not found inside the generated image): out='{cmd.stdout}', err='{cmd.stderr}")

            cmd = ssh_client.exec(
                f"lsinitrd {image_path} | grep 'lib/modules/{kernel_version}'", ignore_rc=True)
            check.equal(
                cmd.rc, 0,
                f"Dracut failed (Kernel modules directory not found inside the image): out='{cmd.stdout}', err='{cmd.stderr}")

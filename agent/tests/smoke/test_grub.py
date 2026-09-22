import pytest
import allure
from typing import Iterator, Tuple
import pytest_check as check
from cyp_test_lib.ssh_client import SshClient


@allure.suite('grub tests')
@pytest.mark.smoke
@pytest.mark.grub
class TestGrub:
    '''Tests for the GRUB bootloader'''

    @pytest.fixture(scope='function')
    def setup_grub_env(self, ssh_client: SshClient, remote_tmp_path: str) -> Iterator[Tuple[str, str, str]]:
        '''
        Fixture to prepare a safe path for generating a dummy config.
        Checks for grub-mkconfig and cleans up afterwards.
        '''

        mkconfig_cmd = 'grub-mkconfig'
        check_cmd = 'grub-script-check'
        cmd = ssh_client.exec('command -v grub-mkconfig', ignore_rc=True)
        if cmd.rc == 0:
            mkconfig_cmd = 'grub-mkconfig'
            check_cmd = 'grub-script-check'
        else:
            cmd = ssh_client.exec('command -v grub2-mkconfig', ignore_rc=True)
            if cmd.rc == 0:
                mkconfig_cmd = 'grub2-mkconfig'
                check_cmd = 'grub2-script-check'
            else:
                pytest.fail(
                    f"Grub failed (Neither 'grub-mkconfig' nor 'grub2-mkconfig' found): out='{cmd.stdout}', err='{cmd.stderr}'")

        dummy_cfg_path = f'{remote_tmp_path}/grub_test.cfg'

        ssh_client.exec(f'rm -f {dummy_cfg_path}', ignore_rc=True)

        yield mkconfig_cmd, check_cmd, dummy_cfg_path

    @allure.title('grub: minimal test (version check)')
    @pytest.mark.minimal
    def test_grub_utilities(self, ssh_client: SshClient):
        '''
        Tests that GRUB user-space tools are installed.
        Doesn't require root privileges.
        '''
        with allure.step('Check grub-mkconfig or grub2-mkconfig version'):
            cmd = ssh_client.exec('grub-mkconfig --version', ignore_rc=True)
            if cmd.rc != 0:
                cmd = ssh_client.exec(
                    'grub2-mkconfig --version', ignore_rc=True)
            assert cmd.rc == 0, f"Grub failed (Neither 'grub-mkconfig' nor 'grub2-mkconfig' found in PATH): out='{cmd.stdout}', err='{cmd.stderr}'"

    @allure.title('grub: generate and verify configuration file')
    def test_grub_config_generation(self, ssh_client: SshClient, setup_grub_env):
        '''
        Tests core GRUB functionality by generating a configuration file
        (scanning kernels and options) and verifying its syntax.
        Requires ROOT.
        '''
        mkconfig_cmd, check_cmd, dummy_cfg_path = setup_grub_env

        with allure.step(f'Generate dummy config to {dummy_cfg_path}'):
            cmd = ssh_client.exec_sudo(
                f'{mkconfig_cmd} -o {dummy_cfg_path}', ignore_rc=True)
            check.equal(
                cmd.rc, 0, f"Grub failed (Config generation failed): out='{cmd.stdout}', err='{cmd.stderr}'")

        check_tool_exists = ssh_client.exec(
                f'command -v {check_cmd}', ignore_rc=True)
        if check_tool_exists.rc == 0:
            with allure.step('Verify that config contains menu entries'):
                cmd = ssh_client.exec_sudo(
                    f"grep 'menuentry' {dummy_cfg_path}", ignore_rc=True)
                check.equal(
                    cmd.rc, 0, f"Grub failed (Generated config seems empty, no menuentry found): out='{cmd.stdout}', err='{cmd.stderr}'")

            with allure.step('Check configuration syntax validity'):
                cmd = ssh_client.exec_sudo(
                    f"{check_cmd} {dummy_cfg_path}", ignore_rc=True)
                check.equal(
                    cmd.rc, 0, f"Grub failed (Generated config has syntax errors): out='{cmd.stdout}', err='{cmd.stderr}'")
        else:
            print(f'Warning: {check_cmd} not found, skipping syntax check')

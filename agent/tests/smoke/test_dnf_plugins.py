import pytest
import allure
import pytest_check as check
from cyp_test_lib.ssh_client import SshClient


@allure.suite('dnf-plugins-core tests')
@pytest.mark.smoke
@pytest.mark.dnf_plugins_core
class TestDnfPluginsCore:
    '''Tests for the dnf-plugins-core package (Integration checks only)'''

    @allure.title('dnf-plugins-core: minimal test')
    @pytest.mark.minimal
    def test_dnf_plugins_core_utilities(self, ssh_client: SshClient):
        '''Tests minimal setup of dnf (entry point for plugins)'''
        with allure.step('Check installation'):
            cmd = ssh_client.exec('dnf --version', ignore_rc=True)
            assert cmd.rc == 0, f"dnf failed (dnf is not installed) out='{cmd.stdout}', err='{cmd.stderr}"

    @allure.title('dnf-plugins-core: check "download" and "config-manager" plugin registration')
    def test_dnf_download_plugin_registered(self, ssh_client: SshClient):
        '''
        Verifies that the 'download' plugin is correctly loaded by DNF.
        Checking '--help' proves the plugin code is loaded and the command exists.
        Tests the 'config-manager' plugin.
        '''
        with allure.step("Check if 'dnf download --help' works"):
            cmd = ssh_client.exec('dnf download --help', ignore_rc=True)

            check.equal(
                cmd.rc, 0, f"Plugin 'download' seems broken or missing. Stderr: {cmd.stderr}")
            check.is_true('Download command-specific options' in cmd.stdout or 'download' in cmd.stdout,
                          f"dnf failed (Help output does not look correct for download plugin.) out='{cmd.stdout}', err='{cmd.stderr}")

        with allure.step('Run dnf config-manager --dump'):
            cmd = ssh_client.exec('dnf config-manager --dump', ignore_rc=True)
            check.equal(
                cmd.rc, 0, f'dnf config-manager execution failed. Stderr: {cmd.stderr}')
            check.is_true('[main]' in cmd.stdout or 'config_file_path' in cmd.stdout or '=' in cmd.stdout,
                          f"dnf failed (Output does not look like a DNF configuration dump) out='{cmd.stdout}', err='{cmd.stderr}")

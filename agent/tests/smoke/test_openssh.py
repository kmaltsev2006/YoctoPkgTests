import pytest
import allure
from cyp_test_lib.ssh_client import SshClient

OPENSSH_BINARY = '/usr/bin/ssh'


@allure.suite('openssh tests')
@pytest.mark.smoke
@pytest.mark.openssh
class TestOpenssh:
    """openssh smoke test class"""

    @allure.title('openssh: binary presence')
    @pytest.mark.minimal
    def test_openssh_binary_presence(self, ssh_client: SshClient) -> None:
        """Check that openssh binary is installed"""
        with allure.step(f'Checking {OPENSSH_BINARY} presence'):
            cmd = ssh_client.exec(f'stat {OPENSSH_BINARY}', ignore_rc=True)

        assert cmd.rc == 0, f'openssh failed (binary presence): out="{cmd.stdout}", err="{cmd.stderr}"'

    @allure.title('openssh: version check')
    @pytest.mark.minimal
    def test_openssh_version(self, ssh_client: SshClient) -> None:
        """Check that ssh binary returns a version"""
        with allure.step(f'Running {OPENSSH_BINARY} -V'):
            cmd = ssh_client.exec(f'{OPENSSH_BINARY} -V', ignore_rc=True)
        assert cmd.rc in (0, 1), f'openssh failed (version check): out="{cmd.stdout}", err="{cmd.stderr}"'

    @allure.title('openssh: functional SSH connection attempt')
    @pytest.mark.minimal
    def test_openssh_functional(self, ssh_client: SshClient) -> None:
        """Run a functional SSH command to verify OpenSSH behavior"""
        with allure.step('Running ssh localhost with short timeout'):
            cmd = ssh_client.exec(
                f'{OPENSSH_BINARY} -o ConnectTimeout=1 -o StrictHostKeyChecking=no '
                'localhost echo SSH_OK',
                ignore_rc=True
            )

        assert 'Permission denied' in cmd.stderr or 'SSH_OK' in cmd.stdout, (
            f'openssh failed (functional): out="{cmd.stdout}", err="{cmd.stderr}"'
        )

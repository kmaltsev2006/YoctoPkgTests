import pytest
import pytest_check as check
import allure
from cyp_test_lib.ssh_client import SshClient

OPENSSH_MISC_BINARIES = [
    'scp',
    'ssh-keygen',
]

@allure.suite('openssh-misc tests')
@pytest.mark.smoke
@pytest.mark.openssh_misc
class TestOpensshMisc:
    """openssh-misc smoke test class"""

    @allure.title('openssh-misc: binaries presence')
    @pytest.mark.minimal
    @pytest.mark.parametrize('bin_name', OPENSSH_MISC_BINARIES)
    def test_openssh_misc_binaries(self, bin_name: str, ssh_client: SshClient):
        """Check that essential openssh-misc binaries are installed"""
        with allure.step(f'Checking /usr/bin/{bin_name} presence'):
            cmd = ssh_client.exec(f'stat /usr/bin/{bin_name}', ignore_rc=True)
            check.equal(cmd.rc, 0, f'{bin_name} failed (binary presence): out="{cmd.stdout}", err="{cmd.stderr}"')

    @allure.title('openssh-misc: ssh-keygen basic functionality')
    @pytest.mark.minimal
    def test_ssh_keygen_functional(self, ssh_client: SshClient, remote_tmp_path: str):
        """Generate a temporary key pair to verify ssh-keygen works"""
        key_path = f'{remote_tmp_path}/id_test'
        with allure.step('Generating SSH key pair'):
            cmd = ssh_client.exec(
                f'ssh-keygen -t rsa -b 2048 -f {key_path} -N "" -q',
                ignore_rc=True
            )
            check.equal(cmd.rc, 0, f'ssh-keygen failed (key generation): out="{cmd.stdout}", err="{cmd.stderr}"')

        with allure.step('Checking that key files were created'):
            cmd_priv = ssh_client.exec(f'stat {key_path}', ignore_rc=True)
            cmd_pub = ssh_client.exec(f'stat {key_path}.pub', ignore_rc=True)
            check.equal(cmd_priv.rc, 0, f'ssh-keygen failed (private key file): out="{cmd_priv.stdout}", err="{cmd_priv.stderr}"')
            check.equal(cmd_pub.rc, 0, f'ssh-keygen failed (public key file): out="{cmd_pub.stdout}", err="{cmd_pub.stderr}"')

    @allure.title('openssh-misc: scp basic functionality')
    @pytest.mark.minimal
    def test_scp_functional(self, ssh_client: SshClient, remote_tmp_path: str):
        """Test scp by copying a temporary file locally"""
        src_file = f'{remote_tmp_path}/test_file.txt'
        dst_file = f'{remote_tmp_path}/copy_file.txt'

        ssh_client.exec(f'echo "OPENSSH_MISC_OK" > {src_file}')

        with allure.step('Copying file using scp locally'):
            cmd = ssh_client.exec(f'scp -o StrictHostKeyChecking=no {src_file} {dst_file}', ignore_rc=True)
            check.equal(cmd.rc, 0, f'scp failed (copying file): out="{cmd.stdout}", err="{cmd.stderr}"')

        with allure.step('Checking that file was copied'):
            cmd_stat = ssh_client.exec(f'stat {dst_file}', ignore_rc=True)
            check.equal(cmd_stat.rc, 0, f'scp failed (file presence): out="{cmd_stat.stdout}", err="{cmd_stat.stderr}"')

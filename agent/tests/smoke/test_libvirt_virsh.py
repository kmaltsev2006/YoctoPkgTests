import pytest
import pytest_check as check
import allure
from cyp_test_lib.ssh_client import SshClient


@allure.suite('libvirt-virsh tests')
@pytest.mark.smoke
@pytest.mark.libvirt_virsh
class TestLibvirtVirsh:
    '''libvirt-virsh smoke test class'''

    @allure.title('libvirt-virsh: binary presence test')
    @pytest.mark.minimal
    def test_virsh_binary_presence(self, ssh_client: SshClient):
        '''Check that virsh binary is installed'''
        with allure.step('Checking /usr/bin/virsh presence'):
            cmd = ssh_client.exec('test -f /usr/bin/virsh', ignore_rc=True)
            assert cmd.rc == 0, f'libvirt-virsh failed (binary missing): out="{cmd.stdout}", err="{cmd.stderr}"'

    @allure.title('libvirt-virsh: version command test')
    @pytest.mark.minimal
    def test_virsh_version(self, ssh_client: SshClient):
        '''Check that virsh --version returns successfully'''
        with allure.step('Running virsh --version'):
            cmd = ssh_client.exec('virsh --version', ignore_rc=True)
            check.equal(cmd.rc, 0, f'libvirt-virsh failed (version command): out="{cmd.stdout}", err="{cmd.stderr}"')
            check.is_true(cmd.stdout.strip(), f'libvirt-virsh failed (version output empty): out="{cmd.stdout}", err="{cmd.stderr}"')

    @allure.title('libvirt-virsh: basic list test')
    @pytest.mark.minimal
    def test_virsh_list_all(
        self,
        ssh_client: SshClient
    ):
        '''Check that virsh list --all runs without crashing'''
        with allure.step('Running virsh list --all'):
            cmd = ssh_client.exec('virsh list --all', ignore_rc=True)
            check.equal(cmd.rc, 0, f'libvirt-virsh failed (list --all): out="{cmd.stdout}", err="{cmd.stderr}"')

import pytest
import allure
from cyp_test_lib.ssh_client import SshClient


@allure.suite('protoc-gen-go tests')
@pytest.mark.smoke
@pytest.mark.protoc_gen_go
class TestProtocGenGo:
    '''protoc-gen-go smoke tests'''

    @allure.title('protoc-gen-go: binary exists')
    @pytest.mark.minimal
    def test_protoc_gen_go_binary_exists(self, ssh_client: SshClient):
        '''Check that protoc-gen-go binary is installed'''
        with allure.step('Check protoc-gen-go binary in PATH'):
            cmd = ssh_client.exec('which protoc-gen-go', ignore_rc=True)
            assert cmd.rc == 0, f'protoc-gen-go failed (binary not found): out="{cmd.stdout}", err="{cmd.stderr}"'

    @allure.title('protoc-gen-go: plugin interface')
    @pytest.mark.minimal
    def test_protoc_gen_go_plugin(self, ssh_client: SshClient):
        '''Check that protoc-gen-go works as protoc plugin'''
        with allure.step('Check protoc-gen-go basic functionality'):
            cmd = ssh_client.exec('protoc-gen-go --help 2>&1', ignore_rc=True)

            if 'command not found' in cmd.stderr.lower():
                cmd2 = ssh_client.exec('protoc-gen-go 2>&1', ignore_rc=True)
                assert cmd2.rc != 127, f'protoc-gen-go failed (command not found): out="{cmd2.stdout}", err="{cmd2.stderr}"'
            else:
                assert cmd.rc != 127, f'protoc-gen-go failed (help command error): out="{cmd.stdout}", err="{cmd.stderr}"'

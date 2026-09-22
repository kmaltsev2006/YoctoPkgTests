import pytest
import allure
import pytest_check as check
from cyp_test_lib.ssh_client import SshClient


@allure.suite('gocov-xml tests')
@pytest.mark.smoke
@pytest.mark.gocov_xml
class TestGocovXml:
    '''gocov-xml smoke tests'''

    @allure.title('gocov-xml: binary exists')
    @pytest.mark.minimal
    def test_gocov_xml_binary_exists(self, ssh_client: SshClient):
        '''Check that gocov-xml binary is installed'''
        with allure.step('Check gocov-xml binary in PATH'):
            cmd = ssh_client.exec('which gocov-xml', ignore_rc=True)
            assert cmd.rc == 0, f'gocov-xml failed (binary not found): out="{cmd.stdout}", err="{cmd.stderr}"'

    @allure.title('gocov-xml: shows help information')
    @pytest.mark.minimal
    def test_gocov_xml_help(self, ssh_client: SshClient):
        '''Check that gocov-xml shows help'''
        with allure.step('Run gocov-xml with --help'):
            cmd = ssh_client.exec('gocov-xml --help', ignore_rc=True)
            if cmd.rc != 0:
                cmd2 = ssh_client.exec('gocov-xml', ignore_rc=True)
                assert cmd2.rc != 127, f'gocov-xml failed (no arguments): out="{cmd2.stdout}", err="{cmd2.stderr}"'
            else:
                check.is_in('gocov-xml', cmd.stdout + cmd.stderr,
                            f'gocov-xml failed (help content): out="{cmd.stdout}", err="{cmd.stderr}"')

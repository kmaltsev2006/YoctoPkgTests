import pytest
import allure
import pytest_check as check
from cyp_test_lib.ssh_client import SshClient


@allure.suite('doxygen tests')
@pytest.mark.smoke
@pytest.mark.doxygen
class TestDoxygen:
    '''Tests for the doxygen documentation generator'''

    @allure.title('doxygen: minimal test')
    @pytest.mark.minimal
    def test_doxygen_utilities(self, ssh_client: SshClient):
        '''Tests minimal setup of Doxygen'''
        with allure.step('Check installation'):
            cmd = ssh_client.exec('doxygen --version', ignore_rc=True)
            assert cmd.rc == 0, f"Doxygen failed (Doxygen is not installed): out='{cmd.stdout}', err='{cmd.stderr}"

    @allure.title('doxygen: generate html documentation from source')
    def test_doxygen_generates_html(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str):
        '''
        Tests that doxygen successfully parses source code and generates
        HTML documentation containing the expected text.
        '''

        ssh_client.put_file(
            f'{test_files_path}/test_doxygen.cpp', remote_tmp_path)

        with allure.step('Generating default Doxyfile'):
            cmd = ssh_client.exec(
                f'cd {remote_tmp_path} && doxygen -g', ignore_rc=True)
            check.equal(
                cmd.rc, 0, f"Doxygen failed (DFailed to generate Doxyfile): out='{cmd.stdout}', err='{cmd.stderr}")

        expected_html_file = f'{remote_tmp_path}/html/index.html'
        unique_string = 'My Test Project'

        with allure.step('Run doxygen to generate documentation'):
            cmd = ssh_client.exec(
                f'cd {remote_tmp_path} && doxygen', ignore_rc=True)
            check.equal(
                cmd.rc, 0, f"Doxygen failed: out='{cmd.stdout}', err='{cmd.stderr}")

        with allure.step(f'Verify that output HTML file exists: {expected_html_file}'):
            cmd = ssh_client.exec(
                f'test -f {expected_html_file}', ignore_rc=True)
            check.equal(cmd.rc, 0, f"Doxygen failed (Output HTML file was not created): out='{cmd.stdout}', err='{cmd.stderr}")

        with allure.step('Verify that documentation contains expected content'):
            cmd = ssh_client.exec(
                f"grep -q '{unique_string}' {expected_html_file}", ignore_rc=True)
            check.equal(
                cmd.rc, 0, f"Doxygen failed (Expected string '{unique_string}' not found in generated HTML): out='{cmd.stdout}', err='{cmd.stderr}")

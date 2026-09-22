import pytest
import allure
import pytest_check as check
from cyp_test_lib.ssh_client import SshClient


@allure.suite('man-pages tests')
@pytest.mark.smoke
@pytest.mark.man_pages
class TestManPages:
    '''Tests for man-pages package (documentation).'''

    @allure.title('man-pages: check directory existence')
    @pytest.mark.minimal
    def test_man_pages_files(self, ssh_client: SshClient):
        """
        Minimal test: checks if the standard directory /usr/share/man exists
        and contains at least one section.
        """
        man_dir = '/usr/share/man'
        with allure.step(f'Check directory {man_dir}'):
            cmd = ssh_client.exec(f'test -d {man_dir}', ignore_rc=True)
            check.equal(cmd.rc, 0, f"Man-pages failed (Directory {man_dir} not found): out='{cmd.stdout}', err='{cmd.stderr}'")

        with allure.step('Check for man1 subdirectory (user commands)'):
            cmd = ssh_client.exec(f'test -d {man_dir}/man1', ignore_rc=True)
            assert cmd.rc == 0, f"Man-pages failed (Section directory {man_dir}/man1 not found): out='{cmd.stdout}', err='{cmd.stderr}'"

    # pylint: disable=unused-argument
    @allure.title('man-pages: run man intro (basic functional check)')
    @pytest.mark.parametrize('are_utils_available', [['man']], indirect=True)
    def test_man_intro_execution(self, ssh_client: SshClient, are_utils_available):
        '''
        Verifies that 'man intro' runs correctly and displays readable text.
        Uses MANPAGER=cat to avoid hanging in 'less'.
        '''
        with allure.step('Run man intro'):
            cmd = ssh_client.exec('MANPAGER=cat man intro', ignore_rc=True)
            check.equal(cmd.rc, 0, f"Man-pages failed (Execution failed): out='{cmd.stdout}', err='{cmd.stderr}'")

        with allure.step('Verify output content'):
            output = cmd.stdout
            is_valid_desc = 'introduction to user commands' in output
            check.is_true(is_valid_desc,
                          f"Man-pages failed (Output mismatch - description): out='{cmd.stdout}', err='{cmd.stderr}'")

            is_valid_footer = 'AUTHOR' in output or 'SEE ALSO' in output
            check.is_true(is_valid_footer,
                          f"Man-pages failed (Output mismatch - structure): out='{cmd.stdout}', err='{cmd.stderr}'")

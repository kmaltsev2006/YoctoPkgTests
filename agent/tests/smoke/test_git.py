import pytest
import allure
import pytest_check as check
from cyp_test_lib.ssh_client import SshClient


@allure.suite('git tests')
@pytest.mark.smoke
@pytest.mark.git
class TestGit:
    '''git smoke test class'''
    @allure.title('git: version test')
    @pytest.mark.minimal
    def test_git_version(self, ssh_client: SshClient):
        '''Test git installed version'''
        with allure.step('Checking git version'):
            cmd = ssh_client.exec('git --version', ignore_rc=True)
            assert cmd.rc == 0, f"git failed (not installed): out='{cmd.stdout}', err='{cmd.stderr}'"

    @allure.title('git: init and commit test')
    @pytest.mark.minimal
    def test_git(self, ssh_client: SshClient, remote_tmp_path: str):
        '''Test complete basic git workflow'''
        # Initialize and configure
        commands = [
            'git init',
            "git config user.email 'smoke-test@example.com'",
            "git config user.name 'Smoke Test'",
            "echo '# Test Project' > README.md",
            'git add README.md',
            "git commit -m 'Initial commit with README'"
        ]
        with allure.step('Executing git init and commit'):
            for command in commands:
                cmd = ssh_client.exec(
                    f'cd {remote_tmp_path} && {command}', ignore_rc=True)
                check.equal(
                    cmd.rc, 0, f"git failed: out='{cmd.stdout}', err='{cmd.stderr}'")
        with allure.step('Verifying the commit'):
            cmd = ssh_client.exec(f'cd {remote_tmp_path} && git log --oneline')
            check.is_in('Initial commit', cmd.stdout,
                        f"git failed (initial commit not found): out='{cmd.stdout}', err='{cmd.stderr}'")
        with allure.step('Checking status is clean'):
            cmd = ssh_client.exec(f'cd {remote_tmp_path} && git status')
            check.is_in('nothing to commit', cmd.stdout.lower(
            ), f"git failed (expected 'nothing to commit'): out='{cmd.stdout}', err='{cmd.stderr}'")

import pytest
import allure
import pytest_check as check
from cyp_test_lib.ssh_client import SshClient


@allure.suite('mstflint tests')
@pytest.mark.smoke
@pytest.mark.mstflint
class TestMstflint:
    '''mstflint smoke tests'''

    @allure.title('mstflint: query help flags')
    def test_mstflint_extended_help(self, ssh_client: SshClient):
        '''Check that mstflint supports extended help flags'''
        with allure.step('Check mstflint -hh for extended help'):
            cmd = ssh_client.exec('mstflint -hh 2>&1', ignore_rc=True)

            if cmd.rc != 0:
                if 'invalid' in cmd.stderr.lower() or 'unrecognized' in cmd.stderr.lower():
                    cmd2 = ssh_client.exec(
                        'mstflint --help 2>&1', ignore_rc=True)
                    check.is_in('Usage:', cmd2.stdout.lower(
                    ), f'mstflint failed (no help flag): out="{cmd2.stdout}", err="{cmd2.stderr}"')
            else:
                check.greater(
                    len(cmd.stdout), 0, f'mstflint -hh produced no output: err="{cmd.stderr}"')

    @allure.title('mstflint tools: help information')
    @pytest.mark.parametrize('tool', ['mstvpd', 'mstconfig', 'mstregdump', 'mstmcra'])
    def test_mstflint_tools_help(self, ssh_client: SshClient, tool: str):
        '''Check that mstflint tools show help information if tool is present'''
        with allure.step(f'Check {tool} availability'):
            cmd_exists = ssh_client.exec(f'command -v {tool}', ignore_rc=True)
            tool_exists = (cmd_exists.rc ==
                           0 and cmd_exists.stdout.strip() != '')

        if not tool_exists:
            allure.attach(
                f'{tool} not installed, skipping help checks', 'info')
            return

        with allure.step(f'Check {tool} help output'):
            cmd_h = ssh_client.exec(f'{tool} -h 2>&1', ignore_rc=True)
            cmd_help = ssh_client.exec(f'{tool} --help 2>&1', ignore_rc=True)

            def looks_like_help(cmd):
                out = cmd.stdout.lower()
                return (
                    cmd.rc == 0 and
                    ('usage:' in out or 'options:' in out or 'help' in out)
                )

            help_ok = looks_like_help(cmd_h) or looks_like_help(cmd_help)

            if not help_ok:
                cmd_run = ssh_client.exec(f'{tool} 2>&1', ignore_rc=True)
                help_ok = (
                    'command not found' not in cmd_run.stderr.lower() and
                    len(cmd_run.stdout.strip()) > 0
                )

        assert help_ok, (
            f'{tool} failed to show usable help: '
            f'-h out="{cmd_h.stdout}", err="{cmd_h.stderr}", '
            f'--help out="{cmd_help.stdout}", err="{cmd_help.stderr}"'
        )

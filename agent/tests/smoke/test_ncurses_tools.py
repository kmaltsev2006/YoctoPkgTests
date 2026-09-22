import pytest
import allure
from cyp_test_lib.ssh_client import SshClient


@allure.suite('ncrurses-tools tests')
@pytest.mark.smoke
@pytest.mark.ncrurses_tools
class TestNcursesTools:
    '''ncrurses-tools smoke test class'''

    @allure.title('ncrurses-tools: check installation')
    @pytest.mark.minimal
    @pytest.mark.parametrize('utility', [
        'clear',
        'infocmp',
        'tabs',
        'tic',
        'toe',
        'tput',
        'tset',
        'share',
        'man',
        'captoinfo',
        'infotocap',
        'reset',
    ])
    def test_ncurses_tools_installation(self, ssh_client: SshClient, utility: str):
        '''Check installed utilities'''
        with allure.step(f'Check {utility} installation'):
            cmd = ssh_client.exec(f'which {utility}', ignore_rc=True)
            assert cmd.rc == 0, f'utility not found: {cmd.stderr}'

    @allure.title('clear: check workability')
    @pytest.mark.minimal
    def test_ncurses_tools_clear(self, ssh_client: SshClient):
        '''Test clear command functionality'''
        with allure.step('Check clear workability'):
            cmd = ssh_client.exec('clear', ignore_rc=True)
            assert cmd.rc == 0, f'clear has failed: {cmd.stderr}'

    @allure.title('infocmp: check workability')
    @pytest.mark.minimal
    def test_ncurses_tools_infocmp(self, ssh_client: SshClient):
        '''Test infocmp command functionality'''
        with allure.step('Check infocmp workability'):
            cmd = ssh_client.exec('infocmp', ignore_rc=True)
            assert cmd.rc == 0 and 'terminfo' in cmd.stdout, f'infocmp is broken: {cmd.stderr}'

    @allure.title('tabs: check workability')
    @pytest.mark.minimal
    def test_ncurses_tools_tabs(self, ssh_client: SshClient):
        '''Test tabs command functionality'''
        with allure.step('Check tabs workability'):
            cmd = ssh_client.exec('tabs -T ansi', ignore_rc=True)
            assert cmd.rc == 0, f'tabs has failed: {cmd.stderr}'

    @allure.title('tic: check workability')
    @pytest.mark.minimal
    def test_ncurses_tools_tic(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str):
        '''Test tic command functionality'''
        with allure.step('Copy test_terminfo.src to target'):
            ssh_client.put_file(
                f'{test_files_path}/test_ncurses_tools/test_terminfo.src', remote_tmp_path)
        with allure.step('Check tic workability'):
            cmd = ssh_client.exec(
                f'tic {remote_tmp_path}/test_terminfo.src', ignore_rc=True)
            assert cmd.rc == 0, f'tic has failed: {cmd.stderr}'

    @allure.title('toe: check workability')
    @pytest.mark.minimal
    def test_ncurses_tools_toe(self, ssh_client: SshClient):
        '''Test toe command functionality'''
        with allure.step('Check toe workability'):
            cmd = ssh_client.exec('toe', ignore_rc=True)
            assert cmd.rc == 0, f'toe has failed: {cmd.stderr}'

    @allure.title('tput: check workability')
    @pytest.mark.minimal
    def test_ncurses_tools_tput(self, ssh_client: SshClient):
        '''Test tput command functionality'''
        with allure.step('Check tput workability'):
            cmd = ssh_client.exec('tput lines', ignore_rc=True)
            assert cmd.rc == 0, f'tput has failed: {cmd.stderr}'

    @allure.title('tset: check workability')
    @pytest.mark.minimal
    def test_ncurses_tools_tset(self, ssh_client: SshClient):
        '''Test tset command functionality'''
        with allure.step('Check tset workability'):
            cmd = ssh_client.exec('tset -Q', ignore_rc=True)
            assert cmd.rc == 0, f'tset has failed: {cmd.stderr}'

    @allure.title('captoinfo: check workability')
    @pytest.mark.minimal
    def test_ncurses_tools_captoinfo(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str):
        '''Test captoinfo command functionality'''
        with allure.step('Copy test.termcap to target'):
            ssh_client.put_file(
                f'{test_files_path}/test_ncurses_tools/test.termcap', remote_tmp_path)
        with allure.step('Check captoinfo workability'):
            cmd = ssh_client.exec(
                f'captoinfo {remote_tmp_path}/test.termcap', ignore_rc=True)
            assert cmd.rc == 0, f'captoinfo has failed: {cmd.stderr}'

    @allure.title('infotocap: check workability')
    @pytest.mark.minimal
    def test_ncurses_tools_infotocap(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str):
        '''Test infotocap command functionality'''
        with allure.step('Copy test_terminfo.src to target and compile it'):
            ssh_client.put_file(
                f'{test_files_path}/test_ncurses_tools/test_terminfo.src', remote_tmp_path)
            ssh_client.exec(f'tic -o {remote_tmp_path} {remote_tmp_path}/test_terminfo.src')
        with allure.step('Check infotocap workability'):
            cmd = ssh_client.exec(
                f'infotocap {remote_tmp_path}/t/test-terminal', ignore_rc=True)
            assert cmd.rc == 0, f'infotocap has failed: {cmd.stderr}'

    @allure.title('reset: check workability')
    @pytest.mark.minimal
    def test_ncurses_tools_reset(self, ssh_client: SshClient):
        '''Test reset command functionality'''
        with allure.step('Check reset workability'):
            cmd = ssh_client.exec('reset', ignore_rc=True)
            assert cmd.rc == 0, f'reset has failed: {cmd.stderr}'

    @allure.title('man: check workability')
    @pytest.mark.minimal
    def test_ncurses_tools_man(self, ssh_client: SshClient):
        '''Test man command functionality'''
        with allure.step('Check man workability'):
            cmd = ssh_client.exec('man man', ignore_rc=True)
            assert cmd.rc == 0, f'man has failed: {cmd.stderr}'

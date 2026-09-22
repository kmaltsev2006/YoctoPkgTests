import pytest
import allure
from cyp_test_lib.ssh_client import SshClient
from helpers import check_elf_file

@allure.suite('ncurses-dev tests')
@pytest.mark.smoke
@pytest.mark.ncurses_dev
class TestNcursesDev:
    '''ncurses-dev smoke test class'''

    @allure.title('ncurses_dev: check header')
    @pytest.mark.minimal
    def test_ncurses_dev_version(self, ssh_client: SshClient):
        '''Testing ncurses installed headers'''
        with allure.step('Check ncurses header'):
            cmd = ssh_client.exec('test -f /usr/include/ncurses.h', ignore_rc=True)
            assert cmd.rc == 0, f'ncurses header not found: {cmd.stderr}'

    @allure.title('ncurses-dev: check shared libraries (libncurses.so)')
    @pytest.mark.minimal
    def test_ncurses_dev_shared_libraries_libncurses(self, ssh_client: SshClient):
        '''Testing ncurses libraries installed'''
        with allure.step('Check libncurses.so'):
            cmd = ssh_client.exec('test -f /usr/lib/libncurses.so')
            assert cmd.rc == 0, f'libncurses.so not found: {cmd.stderr}'

    @allure.title('ncurses-dev: check shared libraries (libtinfo.so)')
    @pytest.mark.minimal
    def test_ncurses_dev_shared_libraries_libtinfo(self, ssh_client: SshClient):
        '''Testing ncurses libraries installed'''
        with allure.step('Check libncurses.so'):
            is_elf, msg = check_elf_file(ssh_client, '/usr/lib/libtinfo.so')
            assert is_elf, msg

    # pylint: disable=unused-argument
    @allure.title('ncurses_dev: check workability')
    @pytest.mark.parametrize('are_utils_available', [['gcc']], indirect=True)
    def test_ncurses_dev_workability(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str, are_utils_available: None):
        '''Testing basic functionality'''
        ssh_client.put_file(
            f'{test_files_path}/test_ncurses.c', remote_tmp_path)

        with allure.step('Compile and run'):
            cmd = ssh_client.exec(f'TERM=xterm TERMINFO=/etc/terminfo/ gcc {remote_tmp_path}/test_ncurses.c -lncurses -o \
                                    {remote_tmp_path}/a.out && {remote_tmp_path}/a.out', ignore_rc=True, get_pty=True)
            assert cmd.rc == 0, f'ncurses-dev is broken: {cmd.stderr}'

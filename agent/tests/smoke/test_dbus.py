import pytest
import allure
from cyp_test_lib.ssh_client import SshClient
from helpers import check_elf_file


@allure.suite('dbus-dev tests')
@pytest.mark.smoke
@pytest.mark.dbus_dev
class TestDbusDev:
    '''Tests for the dbus development library (dbus-dev/libdbus-1-dev)'''


    @allure.title('dbus-dev: libraries test')
    @pytest.mark.minimal
    @pytest.mark.parametrize('lib',
                             [
                                 'libdbus-1.so'
                             ])
    def test_dbus_dev_lib(self, lib: str, ssh_client: SshClient):
        '''Test dbus-dev libraries installed'''
        with allure.step('Checking dbus-dev libraries'):
            is_elf, msg = check_elf_file(ssh_client, f'/usr/lib/{lib}')
            assert is_elf, f'dbus-dev failed: {msg}'

    # pylint: disable=unused-argument
    @allure.title('dbus-dev: compile and link simple application using pkg-config')
    @pytest.mark.parametrize('are_utils_available', [['gcc']], indirect=True)
    def test_dbus_compilation(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str, are_utils_available: None):
        '''
        Tests that we can compile a C program linking against libdbus-1
        using flags provided by pkg-config.
        '''
        ssh_client.put_file(
            f'{test_files_path}/test_dbus.c', remote_tmp_path)

        with allure.step('Compile and run using flags from pkg-config'):
            compile_cmd = f'gcc -o {remote_tmp_path}/test_dbus {remote_tmp_path}/test_dbus.c \
                -I/usr/include/dbus-1.0 -I/usr/lib/dbus-1.0/include -ldbus-1  && {remote_tmp_path}/test_dbus'

            cmd = ssh_client.exec(compile_cmd, ignore_rc=True)
            assert cmd.rc == 0 and 'DBus linked successfully!' in cmd.stdout, f"DBus failed: out='{cmd.stdout}', err='{cmd.stderr}"

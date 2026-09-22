import pytest
import allure
from cyp_test_lib.ssh_client import SshClient
from helpers import check_elf_file


@allure.suite('avahi-dev tests')
@pytest.mark.smoke
@pytest.mark.avahi_dev
class TestAvahiDev:
    '''avahi-dev smoke test class'''

    @allure.title('avahi-dev: headers test')
    @pytest.mark.minimal
    @pytest.mark.parametrize('header',
                             [
                                 'avahi-client/client.h',
                                 'avahi-common/error.h'
                             ])
    def test_avahi_dev_headers(self, header: str, ssh_client: SshClient):
        '''Test avahi-dev installed headers'''
        with allure.step('Checking avahi headers installed'):
            cmd = ssh_client.exec(
                f'stat /usr/include/{header}', ignore_rc=True)
            assert cmd.rc == 0, f"avahi-dev failed (header not found): out='{cmd.stdout}', err='{cmd.stderr}'"

    @allure.title('avahi-dev: libraries test')
    @pytest.mark.minimal
    @pytest.mark.parametrize('lib',
                             [
                                 'libavahi-client.so',
                                 'libavahi-common.so'
                             ])
    def test_avahi_dev_lib(self, lib: str, ssh_client: SshClient):
        '''Test avahi-dev libraries installed'''
        with allure.step('Checking avahi libraries'):
            is_elf, msg = check_elf_file(ssh_client, f'/usr/lib/{lib}')
            assert is_elf, f'avahi-dev failed: {msg}'

    @allure.title('avahi-dev: client initialization test')
    def test_avahi_client_init(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str):
        '''Test avahi client initialization functionality'''
        ssh_client.put_file(
            f'{test_files_path}/test_avahi_dev.c', remote_tmp_path)
        with allure.step('Checking avahi client program'):
            command = f'gcc {remote_tmp_path}/test_avahi_dev.c -o {remote_tmp_path}/test_avahi_dev \
                -lavahi-client -lavahi-common && {remote_tmp_path}/test_avahi_dev'
            cmd = ssh_client.exec(command, ignore_rc=True)
            assert cmd.rc == 0 and 'CLIENT_CREATED_SUCCESSFULLY' in cmd.stdout, f"avahi-dev failed:\
                  out='{cmd.stdout}', err='{cmd.stderr}'"

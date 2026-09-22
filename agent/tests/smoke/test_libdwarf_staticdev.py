import pytest
import allure
from cyp_test_lib.ssh_client import SshClient
from helpers import check_static_lib


@allure.suite('libdwarf-staticdev tests')
@pytest.mark.smoke
@pytest.mark.libdwarf_staticdev
class TestLibdwarfStaticdev:
    '''libdwarf-staticdev smoke tests'''

    @allure.title('libdwarf-staticdev: header files exist')
    @pytest.mark.minimal
    @pytest.mark.parametrize('header', [
        '/usr/include/libdwarf.h',
        '/usr/include/dwarf.h'
    ])
    def test_header_files_exist(self, header, ssh_client: SshClient):
        '''Test that libdwarf development header files exist'''
        with allure.step('Checking libdwarf header files'):
            cmd = ssh_client.exec(f'ls {header}', ignore_rc=True)
            assert cmd.rc == 0, f'libdwarf-staticdev failed (missing {header}): out="{cmd.stdout}", err="{cmd.stderr}"'

    @allure.title('libdwarf-staticdev: static library is valid')
    def test_static_library_valid(self, ssh_client: SshClient):
        '''Test that libdwarf static library is a valid static library'''
        with allure.step('Check libdwarf static library using helper'):
            ok, msg = check_static_lib(ssh_client, '/usr/lib/libdwarf.a')
            assert ok, f'libdwarf-staticdev failed: {msg}'

import pytest
import allure
from cyp_test_lib.ssh_client import SshClient


@allure.suite('rxvt-unicode-terminfo tests')
@pytest.mark.smoke
@pytest.mark.rxvt_unicode_terminfo
class TestRxvtUnicodeTerminfo:
    '''rxvt-unicode-terminfo smoke tests'''

    @allure.title('rxvt-unicode-terminfo: terminfo file exists')
    @pytest.mark.minimal
    def test_terminfo_file_exists(self, ssh_client: SshClient):
        '''Test that rxvt-unicode terminfo files exist'''
        with allure.step('Checking /usr/share/terminfo/r/rxvt-unicode'):
            cmd = ssh_client.exec(
                'ls /usr/share/terminfo/r/rxvt-unicode', ignore_rc=True)
            if cmd.rc != 0:
                cmd = ssh_client.exec(
                    'ls /usr/share/terminfo/r/rxvt', ignore_rc=True)
            assert cmd.rc == 0, f'rxvt-unicode-terminfo failed: out="{cmd.stdout}", err="{cmd.stderr}"'

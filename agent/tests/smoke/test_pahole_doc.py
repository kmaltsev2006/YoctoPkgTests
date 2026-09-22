import pytest
import allure
from cyp_test_lib.ssh_client import SshClient


@allure.suite('pahole-doc tests')
@pytest.mark.smoke
@pytest.mark.pahole_doc
class TestPaholeDoc:
    '''pahole-doc smoke test class'''

    @allure.title('pahole-doc: man page test')
    @pytest.mark.minimal
    def test_pahole_doc_manpage(self, ssh_client: SshClient):
        '''Test pahole man page installed'''
        with allure.step('Checking pahole man page'):
            # Try different man page sections
            man_locations = [
                '/usr/share/man/man1/pahole.1',
                '/usr/share/man/man1/pahole.1.gz',
                '/usr/share/man/man1/pahole.1.bz2'
            ]
            found = False
            last_error = ''
            for man_path in man_locations:
                cmd = ssh_client.exec(f'stat {man_path}', ignore_rc=True)
                if cmd.rc == 0:
                    found = True
                    break
                last_error = f"out='{cmd.stdout}', err='{cmd.stderr}'"
            assert found, f'pahole-doc failed (man page not found): {last_error}'

    @allure.title('pahole-doc: man page content test')
    @pytest.mark.parametrize('are_utils_available', [['man']], indirect=True)
    def test_pahole_manpage_content(self, ssh_client: SshClient, are_utils_available: None):  # pylint: disable=unused-argument
        '''Test pahole man page has content'''
        with allure.step('Checking man page content'):
            cmd = ssh_client.exec(
                'man pahole 2>/dev/null | head -20', ignore_rc=True)
            assert cmd.rc == 0 and cmd.stdout, f"pahole-doc failed: out='{cmd.stdout}', err='{cmd.stderr}'"

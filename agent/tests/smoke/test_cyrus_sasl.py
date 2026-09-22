import pytest
import allure
from cyp_test_lib.ssh_client import SshClient


@allure.suite('cyrus-sasl tests')
@pytest.mark.smoke
@pytest.mark.cyrus_sasl
class TestCyrusSasl:
    '''cyrus-sasl smoke tests'''

    @allure.title('cyrus-sasl: library exists')
    @pytest.mark.minimal
    def test_sasl_library_exists(self, ssh_client: SshClient):
        '''Check that SASL runtime library exists in common library paths'''
        paths_to_check = [
            '/usr/lib*/libcyrus-sasl.so*',
            '/usr/lib*/libsasl2.so*'
        ]

        with allure.step('Checking standard library paths for libcyrus-sasl'):
            found = False
            for path in paths_to_check:
                cmd = ssh_client.exec(f'ls {path}', ignore_rc=True)
                if cmd.rc == 0 and cmd.stdout.strip():
                    found = True
                    break

        assert found, 'SASL library not found — cyrus-sasl not installed'

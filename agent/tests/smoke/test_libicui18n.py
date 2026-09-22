import pytest
import allure
from cyp_test_lib.ssh_client import SshClient

@allure.suite('libicui18n tests')
@pytest.mark.smoke
@pytest.mark.libicui18n
class TestLibicui18n:
    '''libicui18n smoke test class'''

    @allure.title('libicui18n: library test')
    def test_libicui18n_library(self, ssh_client: SshClient) -> None:
        '''Test libicui18n library installed'''
        with allure.step('Search for libicui18n.so in /usr'):
            cmd = ssh_client.exec('find /usr -name "libicui18n.so.*" 2>/dev/null | head -1')
            assert 'libicui18n.so' in cmd.stdout, f'No libicui18n library found: {cmd.stdout}'

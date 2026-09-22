import pytest
import allure
from cyp_test_lib.ssh_client import SshClient

@allure.suite('libcpr-staticdev tests')
@pytest.mark.smoke
@pytest.mark.libcpr_staticdev
class TestLibcprStaticdev:
    '''libcpr-staticdev smoke test class'''

    @allure.title('libcpr-staticdev: static library test')
    def test_libcpr_staticdev_library(self, ssh_client: SshClient):
        '''Test libcpr static library installed'''
        with allure.step('Search for libcpr.a in /usr'):
            cmd = ssh_client.exec('find /usr -name "libcpr.a" 2>/dev/null')
            assert 'libcpr.a' in cmd.stdout, f'No libcpr static library found: {cmd.stdout}'

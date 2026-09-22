import pytest
import allure
from cyp_test_lib.ssh_client import SshClient

@allure.suite('libicudata tests')
@pytest.mark.smoke
@pytest.mark.libicudata
class TestLibicudata:
    '''libicudata smoke test class'''

    @allure.title('libicudata: library test')
    def test_libicudata_library(self, ssh_client: SshClient) -> None:
        '''Test libicudata library installed'''
        with allure.step('Search for libicudata.so in /usr'):
            cmd = ssh_client.exec('find /usr -name "libicudata.so.*" 2>/dev/null | head -1')
            assert 'libicudata.so' in cmd.stdout, f'No libicudata library found: {cmd.stdout}'

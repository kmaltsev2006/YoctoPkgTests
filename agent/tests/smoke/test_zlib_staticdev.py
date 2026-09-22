import pytest
import allure
from cyp_test_lib.ssh_client import SshClient
from helpers import check_static_lib


@allure.suite('zlib-staticdev tests')
@pytest.mark.smoke
@pytest.mark.zlib_staticdev
class TestZlibStaticDev:
    '''zlib-staticdev smoke test class'''

    @allure.title('zlib-staticdev: check static library')
    @pytest.mark.minimal
    def test_zlib_static_library(self, ssh_client: SshClient):
        '''Testing libz static library installed'''
        with allure.step('Check libz.a'):
            is_static, msg = check_static_lib(ssh_client, '/usr/lib/libz.a')
            assert is_static, f"zlib-staticdev failed (static library check failed) out='{msg}', err=''"

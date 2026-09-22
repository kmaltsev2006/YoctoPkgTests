import pytest
import allure
from cyp_test_lib.ssh_client import SshClient
from helpers import check_static_lib


@allure.suite('zstd-staticdev tests')
@pytest.mark.smoke
@pytest.mark.zstd_staticdev
class TestZstdStaticDev:
    '''zstd-staticdev smoke test class'''

    @allure.title('zstd-staticdev: check static library')
    @pytest.mark.minimal
    def test_zstd_static_library(self, ssh_client: SshClient):
        '''Testing libzstd static library installed'''
        with allure.step('Check libzstd.a'):
            is_static, msg = check_static_lib(ssh_client, '/usr/lib/libzstd.a')
            assert is_static, f"zstd-staticdev failed (static library check failed) out='{msg}', err=''"

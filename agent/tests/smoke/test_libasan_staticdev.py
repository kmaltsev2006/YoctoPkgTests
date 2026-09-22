import pytest
import allure
from cyp_test_lib.ssh_client import SshClient
from helpers import check_static_lib


@allure.suite('libasan-staticdev tests')
@pytest.mark.smoke
@pytest.mark.libasan_staticdev
class TestLibasanStaticdev:
    '''libasan-staticdev smoke test class'''

    @allure.title('libasan-staticdev: static library test')
    @pytest.mark.minimal
    def test_libasan_static_lib(self, ssh_client: SshClient):
        '''Test libasan-staticdev static library installed'''
        with allure.step('Checking libasan.a'):
            is_static, msg = check_static_lib(ssh_client, '/usr/lib/libasan.a')
            assert is_static, f'libasan-staticdev failed: {msg}'

import pytest
import allure
from cyp_test_lib.ssh_client import SshClient
from helpers import check_static_lib


@allure.suite('libtsan-staticdev tests')
@pytest.mark.smoke
@pytest.mark.libtsan_staticdev
class TestLibtsanStaticdev:
    '''libtsan-staticdev smoke test class'''

    @allure.title('libtsan-staticdev: static library test')
    @pytest.mark.minimal
    def test_libtsan_static_lib(self, ssh_client: SshClient):
        '''Test libtsan-staticdev static library installed'''
        with allure.step('Checking libtsan'):
            is_static, msg = check_static_lib(ssh_client, '/usr/lib/libtsan.a')
            assert is_static, f'libtsan-staticdev failed: {msg}'

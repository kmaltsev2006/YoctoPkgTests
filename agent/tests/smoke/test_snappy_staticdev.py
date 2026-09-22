import pytest
import allure
from cyp_test_lib.ssh_client import SshClient
from helpers import check_static_lib

@allure.suite('snappy-staticdev tests')
@pytest.mark.smoke
@pytest.mark.snappy_staticdev
class TestSnappyStaticDev:
    '''snappy-staticdev smoke test class'''

    @allure.title('snappy-staticdev: check static library')
    @pytest.mark.minimal
    def test_snappy_static_library(self, ssh_client: SshClient):
        '''Testing snappy static library installed'''
        lib_path = '/usr/lib/libsnappy.a'
        with allure.step(f'Check {lib_path}'):
            is_static_lib, msg = check_static_lib(ssh_client, lib_path)
            assert is_static_lib, f'Static library not found or invalid at {lib_path}: {msg}'

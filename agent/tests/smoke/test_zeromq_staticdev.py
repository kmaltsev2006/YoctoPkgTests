import pytest
import allure
from cyp_test_lib.ssh_client import SshClient
from helpers import check_static_lib


@allure.suite('zeromq-staticdev tests')
@pytest.mark.smoke
@pytest.mark.zeromq_staticdev
class TestZeroMqStaticDev:
    '''zeromq-staticdev smoke test class'''

    @allure.title('zeromq-staticdev: check static library')
    @pytest.mark.minimal
    def test_zeromq_static_library(self, ssh_client: SshClient):
        '''Testing libzmq static library installed'''
        with allure.step('Check libzmq.a'):
            is_static, msg = check_static_lib(ssh_client, '/usr/lib/libzmq.a')
            assert is_static, f"zeromq-staticdev failed (static library check failed) out='{msg}', err=''"

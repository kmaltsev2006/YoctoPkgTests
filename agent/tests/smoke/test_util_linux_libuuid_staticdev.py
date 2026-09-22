import pytest
import allure
from cyp_test_lib.ssh_client import SshClient
from helpers import check_static_lib


@allure.suite('util-linux-libuuid-staticdev tests')
@pytest.mark.smoke
@pytest.mark.util_linux_libuuid_staticdev
class TestUtilLinuxLibuuidStaticDev:
    '''util-linux-libuuid-staticdev smoke test class'''

    @allure.title('util-linux-libuuid-staticdev: check headers')
    @pytest.mark.minimal
    def test_util_linux_libuuid_static_headers(self, ssh_client: SshClient):
        '''Testing libuuid headers installed'''
        with allure.step('Check uuid.h presence'):
            cmd = ssh_client.exec('test -f /usr/include/uuid/uuid.h', ignore_rc=True)
            assert cmd.rc == 0, f"util-linux-libuuid-staticdev failed (headers not found) out='{cmd.stdout}', err='{cmd.stderr}'"

    @allure.title('util-linux-libuuid-staticdev: check static library')
    @pytest.mark.minimal
    def test_util_linux_libuuid_static_library(self, ssh_client: SshClient):
        '''Testing libuuid static library installed'''
        with allure.step('Check libuuid.a'):
            is_static, msg = check_static_lib(ssh_client, '/usr/lib/libuuid.a')
            assert is_static, f"util-linux-libuuid-staticdev failed (static library check failed) out='{msg}', err=''"

    @allure.title('util-linux-libuuid-staticdev: check workability')
    def test_util_linux_libuuid_static_workability(self, ssh_client: SshClient):
        '''Testing static library presence and content via busybox grep'''
        with allure.step('Check for uuid_generate symbol in static lib'):
            cmd = ssh_client.exec('grep -a "uuid_generate" /usr/lib/libuuid.a', ignore_rc=True)
            assert cmd.rc == 0, f"util-linux-libuuid-staticdev failed (symbol not found in static lib) out='{cmd.stdout}', err='{cmd.stderr}'"

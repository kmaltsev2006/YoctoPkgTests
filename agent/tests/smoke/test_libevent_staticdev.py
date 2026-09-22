import pytest
import allure
from cyp_test_lib.ssh_client import SshClient

@allure.suite('libevent-staticdev tests')
@pytest.mark.smoke
@pytest.mark.libevent_staticdev
class TestLibeventStaticdev:
    '''libevent-staticdev smoke test class'''

    @allure.title('libevent-staticdev: static library test')
    def test_libevent_staticdev_library(self, ssh_client: SshClient) -> None:
        '''Test libevent static library installed'''
        with allure.step('Search for libevent.a in /usr'):
            cmd = ssh_client.exec('find /usr -name "libevent.a" 2>/dev/null')
            assert 'libevent.a' in cmd.stdout, f'No libevent static library found: {cmd.stdout}'

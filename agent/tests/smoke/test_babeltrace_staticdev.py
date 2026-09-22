import pytest
import allure
from cyp_test_lib.ssh_client import SshClient
from helpers import check_static_lib


@allure.suite('babeltrace-staticdev tests')
@pytest.mark.smoke
@pytest.mark.babeltrace_staticdev
class TestBabeltraceStaticdev:
    '''babeltrace-staticdev smoke test class'''

    @allure.title('babeltrace-staticdev: headers test')
    @pytest.mark.minimal
    def test_babeltrace_staticdev_headers(self, ssh_client: SshClient):
        '''Test babeltrace-staticdev installed headers'''
        with allure.step('Checking headers installed'):
            cmd = ssh_client.exec(
                'stat /usr/include/babeltrace/babeltrace.h', ignore_rc=True)
            assert cmd.rc == 0, f"babeltrace-staticdev failed (header not found): out='{cmd.stdout}', err='{cmd.stderr}'"

    @allure.title('babeltrace-staticdev: libraries test')
    @pytest.mark.minimal
    def test_babeltrace_staticdev_lib(self, ssh_client: SshClient):
        '''Test babeltrace-staticdev libraries installed'''
        with allure.step('Checking babeltrace-staticdev libraries'):
            is_statc_lib, msg = check_static_lib(
                ssh_client, '/usr/lib/libbabeltrace.a')
            assert is_statc_lib, f'babeltrace-staticdev failed: {msg}'

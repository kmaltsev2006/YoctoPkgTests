import pytest
import allure
from cyp_test_lib.ssh_client import SshClient


@allure.suite('jemalloc tests')
@pytest.mark.smoke
@pytest.mark.jemalloc
class TestJemalloc:
    '''jemalloc smoke test class'''
    @allure.title('jemalloc: version test')
    @pytest.mark.minimal
    def test_jemalloc_version(self, ssh_client: SshClient) -> None:
        '''Test jemalloc version or presence'''
        command = 'stat /usr/lib/libjemalloc.so'
        with allure.step('Checking jemalloc library presence'):
            cmd = ssh_client.exec(command, ignore_rc=True)
            assert cmd.rc == 0, f"jemalloc failed: out='{cmd.stdout}', err='{cmd.stderr}'"

    @allure.title('jemalloc: functional test')
    @pytest.mark.minimal
    def test_jemalloc_functional(self, ssh_client: SshClient) -> None:
        '''Test jemalloc utility functionality'''
        with allure.step('Checking jemalloc jeprof utility'):
            cmd = ssh_client.exec('jeprof --help', ignore_rc=True)
            assert cmd.rc == 0 and 'usage' in cmd.stdout.lower(
            ), f"jeprof failed: out='{cmd.stdout}', err='{cmd.stderr}'"

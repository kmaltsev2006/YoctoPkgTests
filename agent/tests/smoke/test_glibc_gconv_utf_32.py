import pytest
import allure
from cyp_test_lib.ssh_client import SshClient

@allure.suite('glibc-gconv-utf-32 tests')
@pytest.mark.smoke
@pytest.mark.glibc_gconv_utf_32
class TestGlibcGconvUtf32:
    '''glibc-gconv-utf-32 smoke tests'''

    @allure.title('glibc-gconv-utf-32: module exists')
    @pytest.mark.minimal
    def test_glibc_gconv_utf_32_module_exists(self, ssh_client: SshClient):
        '''Check that UTF-32 gconv module exists'''
        with allure.step('Looking for /usr/lib*/gconv/UTF-32.so'):
            cmd = ssh_client.exec('ls /usr/lib*/gconv/UTF-32.so', ignore_rc=True)
            assert cmd.rc == 0, f'UTF-32 gconv module not found: out="{cmd.stdout}", err="{cmd.stderr}"'

    @allure.title('glibc-gconv-utf-32: convert string')
    def test_glibc_gconv_utf_32_conversion(self, ssh_client: SshClient):
        '''Convert a string to UTF-32 and check output is non-empty'''
        with allure.step("Converting 'abc' from UTF-8 to UTF-32 using iconv"):
            cmd = ssh_client.exec("echo 'abc' | iconv -f UTF-8 -t UTF-32", ignore_rc=True)
            assert cmd.rc == 0 and cmd.stdout, f'UTF-32 conversion failed or output empty: out="{cmd.stdout}", err="{cmd.stderr}"'

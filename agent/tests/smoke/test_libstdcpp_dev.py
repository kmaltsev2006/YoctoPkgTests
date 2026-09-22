import pytest
import allure
from cyp_test_lib.ssh_client import SshClient
from helpers import check_elf_file


@allure.suite('libstdc++-dev tests')
@pytest.mark.smoke
@pytest.mark.libstdcpp_dev
class TestLibStdCppDev:
    '''Tests covering libstdc++-dev package (headers and tools).'''

    @allure.title('libstdc++-dev: libraries test')
    @pytest.mark.minimal
    def test_libstdcpp_dev_lib(self, ssh_client: SshClient):
        '''Test libstdc++-dev libraries installed'''
        with allure.step('Checking libstdc++-dev libraries'):
            # Checks for the development symlink
            is_elf, msg = check_elf_file(ssh_client, '/usr/lib/libstdc++.so')
            assert is_elf, msg

    # pylint: disable=unused-argument
    @allure.title('libstdc++-dev: check headers')
    @pytest.mark.minimal
    @pytest.mark.parametrize('are_utils_available', [['g++']], indirect=True)
    def test_libstdcpp_dev_headers(self, ssh_client: SshClient, are_utils_available):
        '''
        Minimal test: Verify that headers like <iostream> can be found.
        '''
        with allure.step('Check if <iostream> can be found'):
            cmd = ssh_client.exec(
                'echo "#include <iostream>" | g++ -x c++ -E -', ignore_rc=True)
            assert cmd.rc == 0, f"Libstdc++-dev failed (Header <iostream> not found): out='{cmd.stdout}', err='{cmd.stderr}'"

    # pylint: disable=unused-argument
    @allure.title('libstdc++-dev: check version macro')
    @pytest.mark.parametrize('are_utils_available', [['g++']], indirect=True)
    def test_libstdcpp_dev_macro(self, ssh_client: SshClient, are_utils_available):
        '''
        Main test: Check that the standard library version macro is defined.
        '''
        with allure.step('Check __GLIBCXX__ definition'):
            cmd = ssh_client.exec(
                'echo "#include <vector>\n#ifndef __GLIBCXX__\n#error Lib failure\n#endif" | g++ -x c++ -c -o /dev/null -', ignore_rc=True)
            assert cmd.rc == 0, f"Libstdc++-dev failed (Macro __GLIBCXX__ not defined): out='{cmd.stdout}', err='{cmd.stderr}'"

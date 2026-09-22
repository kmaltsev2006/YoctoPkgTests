import pytest
import allure
import pytest_check as check
from cyp_test_lib.ssh_client import SshClient
from helpers import check_elf_file


@allure.suite('libstdc++ tests')
@pytest.mark.smoke
@pytest.mark.libstdcpp
class TestLibStdCppRuntime:
    '''Tests covering the main libstdc++ runtime package.'''

    @allure.title('libstdc++: libraries test')
    @pytest.mark.minimal
    def test_libstdcpp_lib(self, ssh_client: SshClient):
        '''Test libstdc++ libraries installed'''
        with allure.step('Checking libstdc++ libraries'):
            # The runtime package usually contains libstdc++.so.6.*
            is_elf, msg = check_elf_file(ssh_client, '/usr/lib/libstdc++.so*')
            assert is_elf, msg

    # pylint: disable=unused-argument
    @allure.title('libstdc++: compile and run (dynamic linkage)')
    @pytest.mark.parametrize('are_utils_available', [['g++']], indirect=True)
    def test_libstdcpp_runtime_package(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str, are_utils_available):
        '''
        Verifies the main libstdc++ package.
        Compiles a C++ program dynamically and runs it.
        '''
        source_path = f'{remote_tmp_path}/test_libstdcpp.cpp'
        binary_path = f'{remote_tmp_path}/test_libstdcpp_run'

        ssh_client.put_file(
            f'{test_files_path}/test_libstdcpp.cpp', remote_tmp_path)

        with allure.step('Compile dynamically with g++'):
            cmd = ssh_client.exec(
                f'g++ {source_path} -o {binary_path}', ignore_rc=True)
            check.equal(cmd.rc, 0, f"Libstdc++ failed (Compilation failed): out='{cmd.stdout}', err='{cmd.stderr}'")

        with allure.step('Run the compiled binary'):
            cmd = ssh_client.exec(binary_path, ignore_rc=True)
            check.equal(cmd.rc, 0, f"Libstdc++ failed (Execution failed): out='{cmd.stdout}', err='{cmd.stderr}'")

            check.is_in('Hello, libstdc++', cmd.stdout,
                        f"Libstdc++ failed (Output verification failed): out='{cmd.stdout}', err='{cmd.stderr}'")

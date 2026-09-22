import pytest
import allure
import pytest_check as check
from cyp_test_lib.ssh_client import SshClient
from helpers import check_static_lib


@allure.suite('libstdc++-staticdev tests')
@pytest.mark.smoke
@pytest.mark.libstdcpp_staticdev
class TestLibStdCppStaticDev:
    '''Tests covering libstdc++-staticdev package.'''

    @allure.title('libstdc++-staticdev: check static libraries')
    @pytest.mark.minimal
    @pytest.mark.parametrize('lib',
                             [
                                 'libstdc++.a',
                                 'libstdc++exp.a',
                                 'libstdc++fs.a',
                             ])
    def test_libstdcpp_staticdev_static_libraries(self, lib: str, ssh_client: SshClient):
        '''Testing libstdc++ static libraries'''
        with allure.step(f'Check {lib}'):
            is_static_lib, msg = check_static_lib(
                ssh_client, f'/usr/lib/{lib}')
            assert is_static_lib, msg

    # pylint: disable=unused-argument
    @allure.title('libstdc++-staticdev: compile and run (static linkage)')
    @pytest.mark.parametrize('are_utils_available', [['g++']], indirect=True)
    def test_libstdcpp_staticdev_compilation(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str, are_utils_available):
        '''
        Verifies the libstdc++-staticdev package.
        Compiles a C++ program with -static flag.
        '''
        source_path = f'{remote_tmp_path}/test_libstdcpp.cpp'
        binary_path = f'{remote_tmp_path}/test_libstdcpp_static'

        ssh_client.put_file(
            f'{test_files_path}/test_libstdcpp.cpp', remote_tmp_path)

        with allure.step('Compile statically'):
            cmd = ssh_client.exec(
                f'g++ {source_path} -o {binary_path} -static', ignore_rc=True)
            check.equal(cmd.rc, 0, f"Libstdc++-staticdev failed (Compilation failed): out='{cmd.stdout}', err='{cmd.stderr}'")

        with allure.step('Run the static binary'):
            cmd = ssh_client.exec(binary_path, ignore_rc=True)
            check.equal(cmd.rc, 0, f"Libstdc++-staticdev failed (Execution failed): out='{cmd.stdout}', err='{cmd.stderr}'")
            check.is_in('Hello, libstdc++', cmd.stdout,
                        f"Libstdc++-staticdev failed (Output verification failed): out='{cmd.stdout}', err='{cmd.stderr}'")

        with allure.step('Verify binary is static using ldd'):
            cmd = ssh_client.exec(f'ldd {binary_path}', ignore_rc=True)
            is_static = 'not a dynamic executable' in (cmd.stdout + cmd.stderr) or cmd.rc != 0
            check.is_true(is_static, f"Libstdc++-staticdev failed (Binary is not static): out='{cmd.stdout}', err='{cmd.stderr}'")

import pytest
import allure
from cyp_test_lib.ssh_client import SshClient


@allure.suite('cpp-symlinks tests')
@pytest.mark.smoke
@pytest.mark.cpp_symlinks
class TestCppSymlinks:
    '''cpp-symlinks smoke tests'''

    @allure.title('cpp-symlinks: symlinks exist')
    @pytest.mark.minimal
    def test_symlinks_exist(self, ssh_client: SshClient):
        '''Check that /usr/bin/cpp and /usr/bin/c++ symlinks exist'''
        with allure.step('Verifying that /usr/bin/cpp and /usr/bin/c++ are symbolic links'):
            cmd = ssh_client.exec('test -L /usr/bin/cpp && test -L /usr/bin/c++', ignore_rc=True)
            assert cmd.rc == 0, 'cpp or c++ symlink is missing'

    # pylint: disable=unused-argument
    @allure.title('cpp-symlinks: compile minimal C++ program')
    @pytest.mark.parametrize('are_utils_available', [['g++']], indirect=True)
    def test_compile_minimal_cpp(
        self,
        ssh_client: SshClient,
        test_files_path: str,
        remote_tmp_path: str,
        are_utils_available: None
    ):
        '''Compile and run a minimal C++ program using return codes only'''
        with allure.step('Creating a minimal C++ program in /tmp/test.cpp'):
            ssh_client.exec(
                'echo "#include <iostream>\nint main(){ return 0; }" '
                f'> {remote_tmp_path}/test.cpp'
            )

        with allure.step('Compiling and running the C++ program'):
            cmd = ssh_client.exec(f'c++ {remote_tmp_path}/test.cpp -o {remote_tmp_path}/test && {remote_tmp_path}/test', ignore_rc=True)
            assert cmd.rc == 0, f'Program failed: {cmd.stderr}'

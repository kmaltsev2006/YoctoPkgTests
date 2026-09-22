import pytest
import allure
import pytest_check as check
from cyp_test_lib.ssh_client import SshClient


@allure.suite('googletest tests')
@pytest.mark.smoke
@pytest.mark.googletest_dev
class TestGoogleTestDev:
    '''Tests for the googletest (gtest) C++ testing framework'''

    @allure.title('googletest-dev: minimal test')
    @pytest.mark.minimal
    def test_googletest_utilities(self, ssh_client: SshClient):
        '''Tests minimal setup of googletest (headers check)'''
        with allure.step('Check headers'):
            cmd = ssh_client.exec(
                'test -f /usr/include/gtest/gtest.h', ignore_rc=True)
            assert cmd.rc == 0, f"GoogleTest failed (Header file not found): out='{cmd.stdout}', err='{cmd.stderr}"

    # pylint: disable=unused-argument
    @allure.title('googletest-dev: compile and run simple unit test')
    @pytest.mark.parametrize('are_utils_available', [['g++']], indirect=True)
    def test_gtest_compile_and_run(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str, are_utils_available: None):
        '''
        Verifies that we can compile a test linking against libgtest and libgtest_main,
        and that the test passes.
        '''
        source_path = f'{remote_tmp_path}/test_gtest.cpp'
        binary_path = f'{remote_tmp_path}/test_gtest_app'

        ssh_client.put_file(
            f'{test_files_path}/test_gtest.cpp', remote_tmp_path)

        with allure.step('Compile with -lgtest -lgtest_main'):
            compile_cmd = f'g++ -o {binary_path} {source_path} -lgtest -lgtest_main'
            cmd = ssh_client.exec(compile_cmd, ignore_rc=True)
            check.equal(
                cmd.rc, 0, f"GoogleTest failed (Compilation failed): out='{cmd.stdout}', err='{cmd.stderr}")

        with allure.step('Run the compiled test application'):
            cmd = ssh_client.exec(binary_path, ignore_rc=True)
            check.equal(
                cmd.rc, 0, f"GoogleTest failed (Test did not passed): out='{cmd.stdout}', err='{cmd.stderr}")
            check.is_in('[  PASSED  ]', cmd.stdout,
                        f"GoogleTest failed (GTest output does not contain '[  PASSED  ]'): out='{cmd.stdout}', err='{cmd.stderr}")
            check.is_in('SmokeTest.IntegerMath', cmd.stdout,
                        f"GoogleTest failed (Specific test case not found): out='{cmd.stdout}', err='{cmd.stderr}")

import pytest
import allure
from cyp_test_lib.ssh_client import SshClient
import pytest_check as check


@allure.suite('libtool tests')
@pytest.mark.smoke
@pytest.mark.libtool
class TestLibtool:
    '''libtool smoke test class'''

    @allure.title('libtool: version test')
    @pytest.mark.minimal
    def test_libtool_version(self, ssh_client: SshClient):
        '''Test libtool version command'''
        with allure.step('Checking libtool version'):
            cmd = ssh_client.exec('libtool --version', ignore_rc=True)
            assert cmd.rc == 0 and 'libtool' in cmd.stdout.lower(), \
                f"libtool failed (not installed): out='{cmd.stdout}', err='{cmd.stderr}'"

    @allure.title('libtool: create simple library test')
    def test_libtool_functional(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str):
        '''Test libtool can create a simple library'''

        with allure.step('Creating simple source files'):
            ssh_client.put_file(
                f'{test_files_path}/test_lib.h', remote_tmp_path)
            ssh_client.put_file(
                f'{test_files_path}/test_lib.c', remote_tmp_path)
            ssh_client.put_file(
                f'{test_files_path}/test_libtool.c', remote_tmp_path)

        with allure.step('Compiling library source with libtool'):
            # Compile object file with libtool (specify tag for C compiler)
            cmd = ssh_client.exec(
                f'cd {remote_tmp_path} && libtool --tag=CC --mode=compile gcc -c test_lib.c',
                ignore_rc=True
            )
            check.equal(
                cmd.rc, 0, f"libtool failed (test_lib.c compilation failed): out='{cmd.stdout}', err='{cmd.stderr}'")

        with allure.step('Compiling main program'):
            # First compile main program
            cmd = ssh_client.exec(
                f'cd {remote_tmp_path} && gcc -c test_libtool.c -I.',
                ignore_rc=True
            )
            check.equal(
                cmd.rc, 0, f"libtool failed (main file compilation failed): out='{cmd.stdout}', err='{cmd.stderr}'")

        with allure.step('Linking with libtool-created library'):
            # Try to link using libtool
            cmd = ssh_client.exec(
                f'cd {remote_tmp_path} && libtool --tag=CC --mode=link gcc -o test_program test_libtool.o test_lib.lo',
                ignore_rc=True
            )

            check.equal(
                cmd.rc, 0, f"libtool failed (linking failed): out='{cmd.stdout}', err='{cmd.stderr}'")

        with allure.step('Running test program'):
            cmd = ssh_client.exec(
                f'{remote_tmp_path}/test_program', ignore_rc=True)
            check.is_in('LIBTOOL_TEST_PASSED', cmd.stdout,
                        f"libtool failed: out='{cmd.stdout}', err='{cmd.stderr}'")

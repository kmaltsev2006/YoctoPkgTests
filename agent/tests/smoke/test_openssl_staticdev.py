import pytest
import pytest_check as check
import allure
from cyp_test_lib.ssh_client import SshClient
from helpers import check_static_lib

OPENSSL_STATIC_LIBS = [
    'libssl.a',
    'libcrypto.a',
]


@allure.suite('openssl-staticdev tests')
@pytest.mark.smoke
@pytest.mark.openssl_staticdev
class TestOpensslStaticdev:
    """openssl-staticdev smoke test class"""

    @allure.title('openssl-staticdev: static libraries presence')
    @pytest.mark.minimal
    @pytest.mark.parametrize('lib', OPENSSL_STATIC_LIBS)
    def test_openssl_static_libraries(self, lib: str, ssh_client: SshClient) -> None:
        """Test that OpenSSL static libraries are installed"""
        with allure.step(f'Checking /usr/lib/{lib} presence'):
            is_static, msg = check_static_lib(ssh_client, f'/usr/lib/{lib}')
            check.is_true(
                is_static,
                f'openssl-staticdev failed (static library presence): out="{msg}"'
            )

    # pylint: disable=duplicate-code
    # pylint: disable=unused-argument
    @allure.title('openssl-staticdev: compile and run test program statically')
    @pytest.mark.parametrize('are_utils_available', [['gcc']], indirect=True)
    def test_openssl_static_compile_run(
        self,
        ssh_client: SshClient,
        remote_tmp_path: str,
        test_files_path: str,
        are_utils_available: None
    ) -> None:
        """Compile and run a small C program linking statically against OpenSSL"""
        remote_source = f'{remote_tmp_path}/test_openssl.c'
        test_binary = f'{remote_tmp_path}/test_openssl_static'

        with allure.step('Copying test source file to remote host'):
            ssh_client.put_file(f'{test_files_path}/test_openssl.c', remote_source)

        with allure.step('Compiling test program statically with -static -lssl -lcrypto'):
            cmd = ssh_client.exec(
                f'gcc -static {remote_source} -lssl -lcrypto -o {test_binary}',
                ignore_rc=True
            )
            check.equal(
                cmd.rc,
                0,
                f'openssl-staticdev failed (compilation): out="{cmd.stdout}", err="{cmd.stderr}"'
            )

        with allure.step('Running compiled test program'):
            cmd = ssh_client.exec(test_binary, ignore_rc=True)
            check.equal(
                cmd.rc,
                0,
                f'openssl-staticdev failed (execution): out="{cmd.stdout}", err="{cmd.stderr}"'
            )
            check.is_in(
                'OPENSSL_OK',
                cmd.stdout,
                f'openssl-staticdev failed (execution output): out="{cmd.stdout}", err="{cmd.stderr}"'
            )

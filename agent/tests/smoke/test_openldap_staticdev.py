import pytest
import pytest_check as check
import allure

from cyp_test_lib.ssh_client import SshClient
from helpers import check_static_lib

OPENLDAP_STATIC_LIBS = [
    'libldap.a',
    'liblber.a',
]

@allure.suite('openldap-staticdev tests')
@pytest.mark.smoke
@pytest.mark.openldap_staticdev
class TestOpenldapStaticdev:
    """openldap-staticdev smoke test class"""

    @allure.title('openldap-staticdev: static libraries presence')
    @pytest.mark.minimal
    @pytest.mark.parametrize('lib', OPENLDAP_STATIC_LIBS)
    def test_openldap_staticdev_libraries(self, lib: str, ssh_client: SshClient):
        """Check that OpenLDAP static libraries are installed"""
        with allure.step(f'Checking {lib} static library presence'):
            is_static, msg = check_static_lib(ssh_client, f'/usr/lib/{lib}')
            check.is_true(is_static, f'OpenLDAP-staticdev failed ({lib}): {msg}')

    # pylint: disable=unused-argument
    @allure.title('openldap-staticdev: compile test program statically')
    @pytest.mark.parametrize('are_utils_available', [['gcc']], indirect=True)
    def test_openldap_staticdev_compile(
        self,
        ssh_client: SshClient,
        remote_tmp_path: str,
        test_files_path: str,
        are_utils_available: None
    ):
        """Compile test program using OpenLDAP static libraries with all TLS deps"""
        remote_source = f'{remote_tmp_path}/test_openldap.c'
        binary = f'{remote_tmp_path}/test_openldap'

        with allure.step('Copying test source to remote host'):
            ssh_client.put_file(f'{test_files_path}/test_openldap.c', remote_source)

        with allure.step('Compiling OpenLDAP static test program with TLS dependencies'):
            cmd = ssh_client.exec(
                f'gcc {remote_source} -o {binary} -static -lldap -llber',
                ignore_rc=True
            )

        check.equal(
            cmd.rc,
            0,
            f'OpenLDAP-staticdev failed (compilation): out="{cmd.stdout}", err="{cmd.stderr}"'
        )

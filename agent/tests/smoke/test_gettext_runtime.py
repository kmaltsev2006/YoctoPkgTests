import pytest
import allure
import pytest_check as check
from cyp_test_lib.ssh_client import SshClient


@allure.suite('gettext-runtime tests')
@pytest.mark.smoke
@pytest.mark.gettext_runtime
class TestGettextRuntime:
    '''gettext-runtime smoke tests (runtime only)'''

    # pylint: disable=unused-argument
    @allure.title('gettext-runtime: binary exists')
    @pytest.mark.minimal
    @pytest.mark.parametrize('are_utils_available', [['gettext']], indirect=True)
    def test_binary_exists(self, ssh_client: SshClient, are_utils_available: None):
        '''Check that gettext binary exists on the system'''
        with allure.step('Checking presence of gettext binary'):
            cmd = ssh_client.exec('which gettext', ignore_rc=True)
            assert cmd.rc == 0, 'gettext binary is missing — gettext-runtime not installed'

    # pylint: disable=unused-argument
    @allure.title('gettext-runtime: run msgfmt on minimal .po')
    @pytest.mark.parametrize('are_utils_available', [['msgfmt']], indirect=True)
    def test_run_msgfmt(
        self,
        ssh_client: SshClient,
        test_files_path: str,
        remote_tmp_path: str,
        are_utils_available: None
    ):
        '''Verify that msgfmt can run on a minimal valid .po file'''
        local_po = f'{test_files_path}/test_gettext_runtime.po'
        remote_po = f'{remote_tmp_path}/test.po'
        remote_mo = f'{remote_tmp_path}/test.mo'

        with allure.step('Uploading minimal valid .po file to DUT'):
            ssh_client.put_file(str(local_po), remote_po)

        with allure.step('Running msgfmt to compile .po to .mo'):
            cmd = ssh_client.exec(f'msgfmt {remote_po} -o {remote_mo}', ignore_rc=True)
            check.equal(cmd.rc, 0, f'msgfmt command failed: {cmd.stderr}')

        with allure.step('Checking that .mo file was created'):
            cmd = ssh_client.exec(f'test -f {remote_mo}', ignore_rc=True)
            check.equal(cmd.rc, 0, '.mo file not created')

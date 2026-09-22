import pytest
import allure
import pytest_check as check
from cyp_test_lib.ssh_client import SshClient


@allure.suite('gettext tests')
@pytest.mark.smoke
@pytest.mark.gettext
class TestGettext:
    '''gettext smoke tests'''

    # pylint: disable=unused-argument
    @allure.title('gettext: binaries exist')
    @pytest.mark.minimal
    @pytest.mark.parametrize('binary', ['gettext', 'msgfmt'])
    @pytest.mark.parametrize('are_utils_available', [['gettext', 'msgfmt']], indirect=True)
    def test_binaries_exist(self, binary: str, ssh_client: SshClient, are_utils_available: None):
        '''Check that gettext and msgfmt binaries are installed'''
        with allure.step(f'Checking that {binary} binary exists'):
            cmd = ssh_client.exec(f'which {binary}', ignore_rc=True)
            assert cmd.rc == 0, f'{binary} not found: {cmd.stderr}'

    # pylint: disable=unused-argument
    @allure.title('gettext: compile .po to .mo')
    @pytest.mark.parametrize('are_utils_available', [['msgfmt']], indirect=True)
    def test_compile_po(
        self,
        ssh_client: SshClient,
        test_files_path: str,
        remote_tmp_path: str,
        are_utils_available: None
    ):
        '''Upload .po file and compile it to .mo'''
        local_po = f'{test_files_path}/test_gettext.po'
        remote_po = f'{remote_tmp_path}/test.po'
        remote_mo = f'{remote_tmp_path}/test.mo'

        with allure.step(f'Uploading {local_po} to {remote_po}'):
            ssh_client.put_file(local_po, remote_po)

        with allure.step('Compiling PO -> MO with msgfmt'):
            cmd = ssh_client.exec(f'msgfmt {remote_po} -o {remote_mo}', ignore_rc=True)
            check.equal(cmd.rc, 0, f'msgfmt failed: {cmd.stderr}')

        with allure.step(f'Checking that .mo file was created at {remote_mo}'):
            cmd = ssh_client.exec(f'test -f {remote_mo}', ignore_rc=True)
            check.equal(cmd.rc, 0, '.mo file not created')

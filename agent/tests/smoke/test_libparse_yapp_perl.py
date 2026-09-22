import pytest
import allure
import pytest_check as check
from cyp_test_lib.ssh_client import SshClient


@allure.suite('libparse-yapp-perl tests')
@pytest.mark.smoke
@pytest.mark.libparse_yapp_perl
class TestLibParseYappPerl:
    '''Tests for the libparse-yapp-perl package.'''

    # pylint: disable=unused-argument
    @allure.title('libparse-yapp-perl: minimal module check')
    @pytest.mark.minimal
    @pytest.mark.parametrize('are_utils_available', [['perl']], indirect=True)
    def test_libparse_yapp_minimal(self, ssh_client: SshClient, are_utils_available):
        '''Tests minimal setup: verify Parse::Yapp can be loaded via command line.'''
        with allure.step('Check if Parse::Yapp module loads'):
            cmd = ssh_client.exec('perl -MParse::Yapp -e 1', ignore_rc=True)
            assert cmd.rc == 0, f"Libparse-yapp-perl failed (Module load failed): out='{cmd.stdout}', err='{cmd.stderr}'"

    # pylint: disable=unused-argument
    @allure.title('libparse-yapp-perl: run usage script')
    @pytest.mark.parametrize('are_utils_available', [['perl']], indirect=True)
    def test_libparse_yapp_usage(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str, are_utils_available):
        '''
        Verifies that the Perl script using Parse::Yapp runs correctly.
        '''
        script_path = f'{remote_tmp_path}/test_libparse_yapp.pl'

        ssh_client.put_file(
            f'{test_files_path}/test_libparse_yapp.pl', remote_tmp_path)

        with allure.step('Run the Perl script'):
            cmd = ssh_client.exec(f'perl {script_path}', ignore_rc=True)

            check.equal(cmd.rc, 0, f"Libparse-yapp-perl failed (Script execution failed): out='{cmd.stdout}', err='{cmd.stderr}'")
            check.is_in('Module loaded successfully', cmd.stdout,
                        f"Libparse-yapp-perl failed (Output mismatch): out='{cmd.stdout}', err='{cmd.stderr}'")

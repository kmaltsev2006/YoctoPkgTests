import pytest
import allure
import pytest_check as check
from cyp_test_lib.ssh_client import SshClient


@allure.suite('libjson-perl tests')
@pytest.mark.smoke
@pytest.mark.libjson_perl
class TestLibJsonPerl:
    '''Tests for the libjson-perl module.'''

    @allure.title('libjson-perl: minimal test')
    @pytest.mark.minimal
    def test_libjson_perl_utilities(self, ssh_client: SshClient):
        '''Tests minimal setup of libjson-perl (module load check)'''
        with allure.step('Check if JSON module can be loaded'):
            cmd = ssh_client.exec('perl -MJSON -e 1', ignore_rc=True)
            assert cmd.rc == 0, f"Libjson-perl failed (Perl module 'JSON' cannot be loaded): out='{cmd.stdout}', err='{cmd.stderr}'"

    # pylint: disable=unused-argument
    @allure.title('libjson-perl: encode and decode JSON data')
    @pytest.mark.parametrize('are_utils_available', [['perl']], indirect=True)
    def test_json_perl_functionality(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str, are_utils_available: None):
        '''
        Verifies that the JSON module works correctly by running a Perl script
        that encodes and decodes JSON data.
        '''
        script_path = f'{remote_tmp_path}/test_libjson.pl'

        ssh_client.put_file(
            f'{test_files_path}/test_libjson.pl', remote_tmp_path)

        with allure.step('Run the Perl script'):
            cmd = ssh_client.exec(f'perl {script_path}', ignore_rc=True)
            check.equal(cmd.rc, 0, f"Libjson-perl failed (Script execution failed): out='{cmd.stdout}', err='{cmd.stderr}'")

        with allure.step('Verify output'):
            check.is_in('Encoded:', cmd.stdout,
                        f"Libjson-perl failed (JSON encoding failed): out='{cmd.stdout}', err='{cmd.stderr}'")

            check.is_true('"status":"active"' in cmd.stdout or '"status" : "active"' in cmd.stdout,
                          f"Libjson-perl failed (Encoded JSON structure incorrect): out='{cmd.stdout}', err='{cmd.stderr}'")

            check.is_in('Decoded successfully', cmd.stdout,
                        f"Libjson-perl failed (JSON decoding check failed): out='{cmd.stdout}', err='{cmd.stderr}'")

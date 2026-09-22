import pytest
import allure
import pytest_check as check
from cyp_test_lib.ssh_client import SshClient


@allure.suite('di tests')
@pytest.mark.smoke
@pytest.mark.di
class TestDi:
    '''Tests for the di (Disk Information) utility'''

    @allure.title('di: check basic text output and headers')
    def test_di_basic_output(self, ssh_client: SshClient):
        '''
        Runs 'di' without arguments and checks if standard table headers are present.
        Based on the screenshot provided.
        '''
        with allure.step("Check that 'di' is installed"):
            cmd = ssh_client.exec('command -v di', ignore_rc=True)
            assert cmd.rc == 0, f"di failed (di is not installed) out='{cmd.stdout}', err='{cmd.stderr}"

        with allure.step("Run 'di' and verify table headers"):
            cmd = ssh_client.exec('di', ignore_rc=True)
            assert cmd.rc == 0, f"di failed (Execution failed) out='{cmd.stdout}', err='{cmd.stderr}"

            output = cmd.stdout
            headers = ['Filesystem', 'Mount', 'Size', 'Type']
            for header in headers:
                check.is_in(header, output, f"di failed (Header {header} is missing) out='{cmd.stdout}', err='{cmd.stderr}")

        with allure.step("Run 'di -t'"):
            cmd = ssh_client.exec('di -t', ignore_rc=True)
            check.equal(cmd.rc, 0, f'di failed: {cmd.stderr}')
            assert 'Total' in cmd.stdout, f"di failed (Flag -t did not produce 'Total' summary line) out='{cmd.stdout}', err='{cmd.stderr}"

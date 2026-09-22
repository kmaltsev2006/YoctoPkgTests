import pytest
import pytest_check as check
import allure

from cyp_test_lib.ssh_client import SshClient


@allure.suite('nvme-cli tests')
@pytest.mark.smoke
@pytest.mark.nvme_cli
class TestNvmeCli:
    """nvme-cli smoke test class"""

    @allure.title('nvme-cli: version command')
    @pytest.mark.minimal
    def test_nvme_cli_version(self, ssh_client: SshClient):
        """Test that nvme version command works"""
        with allure.step('Running nvme version command'):
            cmd = ssh_client.exec('nvme version', ignore_rc=True)
            assert cmd.stdout.strip(), f'nvme-cli failed (version): out="{cmd.stdout}", err="{cmd.stderr}"'

    # pylint: disable=unused-argument
    @allure.title('nvme-cli: compile and run test program')
    @pytest.mark.parametrize('are_utils_available', [['gcc']], indirect=True)
    def test_nvme_cli_compile_run(
        self,
        ssh_client: SshClient,
        remote_tmp_path: str,
        test_files_path: str,
        are_utils_available: None
    ):
        """Compile and run small test program using libnvme"""
        remote_source = f'{remote_tmp_path}/test_nvme.c'
        test_binary = f'{remote_tmp_path}/test_nvme'

        with allure.step('Copying test source file to remote host'):
            ssh_client.put_file(f'{test_files_path}/test_nvme.c', remote_source)

        with allure.step('Compiling test program with libnvme'):
            cmd = ssh_client.exec(f'gcc {remote_source} -lnvme -o {test_binary}', ignore_rc=True)
            check.equal(cmd.rc, 0, f'nvme-cli failed (compile): out="{cmd.stdout}", err="{cmd.stderr}"')

        with allure.step('Running compiled test program'):
            cmd = ssh_client.exec(test_binary, ignore_rc=True)
            check.equal(cmd.rc, 0, f'nvme-cli failed (run): out="{cmd.stdout}", err="{cmd.stderr}"')
            check.is_true(cmd.stdout.strip(), f'nvme-cli failed (output): out="{cmd.stdout}", err="{cmd.stderr}"')

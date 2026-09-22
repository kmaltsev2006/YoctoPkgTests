import pytest
import allure
import pytest_check as check
from cyp_test_lib.ssh_client import SshClient


@allure.suite('pahole tests')
@pytest.mark.smoke
@pytest.mark.pahole
class TestPahole:
    '''pahole smoke test class'''

    @allure.title('pahole: version test')
    @pytest.mark.minimal
    def test_pahole_version(self, ssh_client: SshClient):
        '''Test pahole version command'''
        with allure.step('Checking pahole version'):
            cmd = ssh_client.exec('pahole --version', ignore_rc=True)
            assert cmd.rc == 0, f"pahole failed (not installed): out='{cmd.stdout}', err='{cmd.stderr}'"

    @allure.title('pahole: functionality test')
    def test_pahole_elf_analysis(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str):
        '''Test pahole ELF file analysis functionality'''
        with allure.step('Creating simple ELF file for testing'):
            ssh_client.put_file(
                f'{test_files_path}/test_pahole.c', remote_tmp_path)
            test_file = f'{remote_tmp_path}/test_pahole.c'
            test_binary = f'{remote_tmp_path}/pahole_test'

            cmd = ssh_client.exec(
                f'gcc -g {test_file} -o {test_binary}',
                ignore_rc=True
            )
            check.equal(
                cmd.rc, 0, f"pahole failed (compile error): out='{cmd.stdout}', err='{cmd.stderr}'")

        with allure.step('Running pahole on compiled binary'):
            cmd = ssh_client.exec(f'pahole {test_binary}', ignore_rc=True)
            # pahole should output something about structures or types
            check.is_in('test_struct', cmd.stdout or cmd.stderr,
                        f"pahole failed (test_struct expected): out='{cmd.stdout}', err='{cmd.stderr}'")

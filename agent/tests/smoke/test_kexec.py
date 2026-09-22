import pytest
import allure
from cyp_test_lib.ssh_client import SshClient


@allure.suite('kexec tests')
@pytest.mark.smoke
@pytest.mark.kexec
class TestKexec:
    '''kexec smoke test class'''

    @allure.title('kexec: version test')
    @pytest.mark.minimal
    def test_kexec_version(self, ssh_client: SshClient):
        '''Test kexec version command'''
        with allure.step('Checking kexec version'):
            cmd = ssh_client.exec('kexec --version', ignore_rc=True)
            assert cmd.rc == 0, f"kexeg failed (not installed): out='{cmd.stdout}', err='{cmd.stderr}'"

    @allure.title('kexec: kernel parsing test')
    @pytest.mark.minimal
    def test_kexec_kernel_parsing(self, ssh_client: SshClient):
        '''Test kexec can parse kernel'''
        with allure.step('Finding kernel file'):
            cmd = ssh_client.exec(
                'ls /boot/bzImage* 2>/dev/null | head -1',
                ignore_rc=True
            )
            if cmd.rc != 0 or not cmd.stdout.strip():
                pytest.skip('No bzImage found for testing')

            kernel = cmd.stdout.strip()

        with allure.step('Testing kexec parse capabilities'):
            cmd = ssh_client.exec(
                f'kexec -l {kernel} --no-ifdown 2>&1',
                ignore_rc=True
            )
            output = cmd.stdout + cmd.stderr
            expected_patterns = [
                'entry',
                'nr_segments',
                'segment[',
                '.buf',
                '.mem',
                'kexec_load failed'  # This is expected in many cases
            ]
            patterns_found = sum(
                1 for pattern in expected_patterns if pattern in output)
            assert patterns_found >= 1, \
                f"kexec failed (expected parsing output): Found {patterns_found} patterns; out='{cmd.stdout}', err='{cmd.stderr}'"
            cmd = ssh_client.exec(
                'kexec -u',
                ignore_rc=True
            )

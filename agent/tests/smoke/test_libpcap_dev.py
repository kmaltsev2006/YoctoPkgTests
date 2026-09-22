import pytest
import allure
import pytest_check as check
from cyp_test_lib.ssh_client import SshClient
from helpers import check_elf_file


@allure.suite('libpcap tests')
@pytest.mark.smoke
@pytest.mark.libpcap
class TestLibPcapDev:
    '''Tests for libpcap-dev package.'''

    @allure.title('libpcap-dev: libraries test')
    @pytest.mark.minimal
    def test_libpcap_dev_lib(self, ssh_client: SshClient):
        '''Test libpcap-dev libraries installed'''
        with allure.step('Checking libpcap-dev libraries'):
            is_elf, msg = check_elf_file(ssh_client, '/usr/lib/libpcap.so')
            assert is_elf, msg

    @allure.title('libpcap-dev: headers test')
    @pytest.mark.minimal
    def test_libpcap_headers(self, ssh_client: SshClient):
        '''Test installed headers'''
        with allure.step('Checking headers installed'):
            cmd = ssh_client.exec(
                'test -f /usr/include/pcap/pcap.h', ignore_rc=True)
            assert cmd.rc == 0, f"Libpcap-dev failed (Header file 'pcap/pcap.h' not found): out='{cmd.stdout}', err='{cmd.stderr}'"

    # pylint: disable=unused-argument
    @allure.title('libpcap-dev: compile and run (pcap_open_dead)')
    @pytest.mark.parametrize('are_utils_available', [['gcc']], indirect=True)
    def test_libpcap_functionality(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str, are_utils_available):
        '''
        Verifies that a C program linking against libpcap compiles and runs correctly.
        Uses pcap_open_dead to ensure safe execution without root privileges.
        '''
        source_path = f'{remote_tmp_path}/test_libpcap.c'
        binary_path = f'{remote_tmp_path}/test_libpcap_bin'

        ssh_client.put_file(
            f'{test_files_path}/test_libpcap.c', remote_tmp_path)

        with allure.step('Compile dynamically with -lpcap'):
            cmd = ssh_client.exec(
                f'gcc {source_path} -o {binary_path} -lpcap', ignore_rc=True)
            check.equal(cmd.rc, 0, f"Libpcap failed (Compilation failed): out='{cmd.stdout}', err='{cmd.stderr}'")

        with allure.step('Run the compiled binary'):
            cmd = ssh_client.exec(binary_path, ignore_rc=True)
            check.equal(cmd.rc, 0, f"Libpcap failed (Execution failed): out='{cmd.stdout}', err='{cmd.stderr}'")

            check.is_in('libpcap initialized successfully', cmd.stdout,
                        f"Libpcap failed (Output verification failed): out='{cmd.stdout}', err='{cmd.stderr}'")

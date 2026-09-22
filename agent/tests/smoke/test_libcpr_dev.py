import pytest
import allure
from cyp_test_lib.ssh_client import SshClient
from helpers import check_elf_file


@allure.suite('libcpr-dev tests')
@pytest.mark.smoke
@pytest.mark.libcpr_dev
class TestLibcprDev:
    '''libcpr-dev smoke test class'''

    @allure.title('libcpr-dev: headers test')
    @pytest.mark.minimal
    def test_libcpr_dev_headers(self, ssh_client: SshClient):
        '''Test libcpr-dev installed headers'''
        with allure.step('Check if cpr.h exists'):
            cmd = ssh_client.exec('stat /usr/include/cpr/cpr.h', ignore_rc=True)
            assert cmd.rc == 0, f'libcpr headers not found: {cmd.stderr}'

    @allure.title('libcpr-dev: library test')
    @pytest.mark.minimal
    def test_libcpr_dev_library(self, ssh_client: SshClient):
        '''Test libcpr-dev library installed'''
        with allure.step('Check if libcpr.so is a valid ELF file'):
            is_elf, msg = check_elf_file(ssh_client, '/usr/lib/libcpr.so')
            assert is_elf, msg

    # pylint: disable=unused-argument
    @allure.title('libcpr-dev: compile test')
    @pytest.mark.parametrize('are_utils_available', [['g++']], indirect=True)
    def test_libcpr_dev_compile(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str, are_utils_available: None):
        '''Testing libcpr-dev workability'''

        with allure.step('Upload test source file'):
            ssh_client.put_file(
                f'{test_files_path}/test_cpr.cpp', remote_tmp_path)

        with allure.step('Compile'):
            cmd = ssh_client.exec(f"g++ {remote_tmp_path}/test_cpr.cpp -o {remote_tmp_path}/test_cpr -lcpr -lcurl && \
                {remote_tmp_path}/test_cpr 2>&1 | head -10", ignore_rc=True)
            assert 'CPR_LIB_WORKS' in cmd.stdout or 'undefined reference' not in cmd.stderr, \
                f'libcpr compilation failed: {cmd.stderr}'

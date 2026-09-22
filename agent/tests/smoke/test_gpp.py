import pytest
import allure
from cyp_test_lib.ssh_client import SshClient


@allure.suite('g++ tests')
@pytest.mark.smoke
@pytest.mark.gpp
class TestGpp:
    '''g++ smoke test class'''
    @allure.title('g++: version test')
    @pytest.mark.minimal
    def test_gpp_version(self, ssh_client: SshClient):
        '''Checking g++ version'''
        with allure.step('Checking g++ version'):
            cmd = ssh_client.exec('g++ --version', ignore_rc=True)
            assert cmd.rc == 0, f"g++ failed (not installed): out='{cmd.stdout}', err='{cmd.stderr}'"

    @allure.title('g++: compile test')
    @pytest.mark.minimal
    def test_gpp(self, ssh_client: SshClient, remote_tmp_path: str):
        '''Checking g++ compilation functionality'''
        code = r'''
        #include <iostream>
        int main() {std::cout<<"Hello!\n"; return 0;}
        '''
        source_filepath = f'{remote_tmp_path}/gpp_test.cpp'
        binary_filepath = f'{remote_tmp_path}/gpp_test'
        with allure.step('Checking g++ compilation'):
            command = f"echo '{code}' > {source_filepath} && \
                        g++ {source_filepath} -o {binary_filepath} && {binary_filepath}"
            cmd = ssh_client.exec(command, ignore_rc=True)
            assert cmd.rc == 0 and 'Hello!' in cmd.stdout, f"g++ failed: out='{cmd.stdout}', err='{cmd.stderr}'"

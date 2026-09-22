import pytest
import allure
import pytest_check as check
from cyp_test_lib.ssh_client import SshClient


@allure.suite('ninja tests')
@pytest.mark.smoke
@pytest.mark.ninja
class TestNinja:
    '''Ninja smoke test class'''


    @allure.title('ninja: minimal test')
    @pytest.mark.minimal
    def test_ninja_utilities(self, ssh_client: SshClient):
        '''Tests minimal setup of Ninja'''
        with allure.step('Check installation'):
            cmd = ssh_client.exec('ninja --version', ignore_rc=True)
            assert cmd.rc == 0, f"Ninja failed (Ninja is not installed): out='{cmd.stdout}', err='{cmd.stderr}'"

    # pylint: disable=unused-argument
    @allure.title('ninja: full cycle (generate, build, run)')
    @pytest.mark.parametrize('are_utils_available', [['g++', 'cmake']], indirect=True)
    def test_ninja_full_cycle(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str, are_utils_available: None):
        '''
        Tests the full build lifecycle using Ninja:
        1. Generates `build.ninja` files using CMake.
        2. Builds the project by calling `ninja`.
        3. Runs the executable and checks the output.
        '''
        files = ['main.cpp', 'CMakeLists.txt']
        for file in files:
            ssh_client.put_file(
                f'{test_files_path}/test_ninja/{file}', remote_tmp_path)
        ssh_client.create_remote_dir(f'{remote_tmp_path}/build')

        build_dir = f'{remote_tmp_path}/build'

        with allure.step("Generating 'build.ninja' files using CMake"):
            command_generate = f'cd {build_dir} && cmake -G Ninja {remote_tmp_path}'
            cmd = ssh_client.exec(command_generate, ignore_rc=True)
            check.equal(
                cmd.rc, 0, f"Ninja failed (Generation failed): out='{cmd.stdout}', err='{cmd.stderr}'")

        with allure.step('Building the project using ninja'):
            command_build = f'cd {build_dir} && ninja'
            cmd = ssh_client.exec(command_build, ignore_rc=True)
            check.equal(
                cmd.rc, 0, f"Ninja failed: out='{cmd.stdout}', err='{cmd.stderr}'")

        with allure.step('Running the application and checking output'):
            executable_path = f'{build_dir}/my_ninja_app'
            cmd = ssh_client.exec(executable_path, ignore_rc=True)
            check.equal(
                cmd.rc, 0, f"Ninja failed: out='{cmd.stdout}', err='{cmd.stderr}'")
            check.is_in('Hello, Ninja!',  cmd.stdout,
                        f"Ninja failed (Unexpeted output): out='{cmd.stdout}', err='{cmd.stderr}'")

import pytest
import allure
from cyp_test_lib.ssh_client import SshClient


@allure.suite('nlohmann-json tests')
@pytest.mark.smoke
@pytest.mark.nlohmann_json
@pytest.mark.nlohmann_json_dev
class TestNlohmannJson:
    '''nlohmann-json smoke test class'''

    @allure.title('nlohmann_json: check header')
    @pytest.mark.minimal
    def test_nlohmann_json_version(self, ssh_client: SshClient):
        '''Testing nlohmann-json installed headers'''
        with allure.step('Check nlohmann-json headers'):
            cmd = ssh_client.exec('test -e /usr/include/nlohmann', ignore_rc=True)
            assert cmd.rc == 0, f'nlohmann-json header not found: {cmd.stderr}'

    # pylint: disable=unused-argument
    @allure.title('nlohmann_json: check workability')
    @pytest.mark.parametrize('are_utils_available', [['g++']], indirect=True)
    def test_nlohmann_json_workability(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str, are_utils_available: None):
        '''Testing basic functionality'''
        ssh_client.put_file(
            f'{test_files_path}/test_nlohmann_json.cpp', remote_tmp_path)

        with allure.step('Compile and run'):
            cmd = ssh_client.exec(f'g++ {remote_tmp_path}/test_nlohmann_json.cpp -o \
                                    {remote_tmp_path}/a.out && {remote_tmp_path}/a.out', ignore_rc=True)
            assert cmd.rc == 0, f'nlohmann-json is broken: {cmd.stderr}'

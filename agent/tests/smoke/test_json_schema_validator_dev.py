import pytest
import allure
from cyp_test_lib.ssh_client import SshClient
from helpers import check_elf_file


@allure.suite('json-schema-validator-dev tests')
@pytest.mark.smoke
@pytest.mark.json_schema_validator_dev
class TestJsonSchemaValidatorDev:
    '''json-schema-validator-dev smoke test class'''

    @allure.title('json_schema_validator-dev: headers test')
    @pytest.mark.minimal
    def test_json_schema_validator_dev_headers(self, ssh_client: SshClient):
        '''Test json-schema-validator headers'''
        with allure.step('Checking json-schema-validator headers are installed'):
            cmd = ssh_client.exec(
                'stat /usr/include/nlohmann/json-schema.hpp', ignore_rc=True)
            assert cmd.rc == 0, f"json-schema-validator-dev failed (header not found): out='{cmd.stdout}', err='{cmd.stderr}'"

    @allure.title('json_schema_validator-dev: libraries test')
    @pytest.mark.minimal
    def test_json_schema_validator_dev_lib(self, ssh_client: SshClient):
        '''Test json-schema-validator-dev libraries installed'''
        with allure.step('Checking json_schema_validator-dev libraries'):
            is_elf, msg = check_elf_file(
                ssh_client, '/usr/lib/libnlohmann_json_schema_validator.so')
            assert is_elf, f'json-schema-validator-dev failed: {msg}'

    @allure.title('json-schema-validator-dev: compile and run test')
    def test_json_schema_validator_dev(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str):
        '''Test json-schema-validator library with basic validation'''
        ssh_client.put_file(
            f'{test_files_path}/test_jsonschema.cpp', remote_tmp_path)
        command = (
            f'g++ {remote_tmp_path}/test_jsonschema.cpp -o {remote_tmp_path}/test_jsonschema '
            f' -lnlohmann_json_schema_validator && {remote_tmp_path}/test_jsonschema'
        )
        with allure.step('Compiling program with json validation'):
            cmd = ssh_client.exec(command, ignore_rc=True)
            assert cmd.rc == 0 and '{"height":10,"width":20}' in cmd.stdout, \
                f"json-schema-validator-dev failed: out='{cmd.stdout}', err='{cmd.stderr}'"

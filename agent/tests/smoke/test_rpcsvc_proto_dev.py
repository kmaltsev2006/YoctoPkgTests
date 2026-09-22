import pytest
import allure
import pytest_check as check
from cyp_test_lib.ssh_client import SshClient

@allure.suite('rpcsvc-proto-dev tests')
@pytest.mark.smoke
@pytest.mark.rpcsvc_proto_dev
class TestRpcsvcProtoDev:
    '''rpcsvc-proto-dev smoke test class'''

    @allure.title('rpcsvc-proto-dev: check rpcgen presence')
    @pytest.mark.minimal
    def test_rpcsvc_proto_dev_rpcgen(self, ssh_client: SshClient):
        '''Check rpcgen utility (often part of dev package)'''
        with allure.step('Check rpcgen installation'):
            cmd = ssh_client.exec('which rpcgen', ignore_rc=True)
            assert cmd.rc == 0, f'rpcgen utility not found: {cmd.stderr}'

    @allure.title('rpcsvc-proto-dev: check development headers')
    @pytest.mark.minimal
    @pytest.mark.parametrize('header', [
        '/usr/include/rpcsvc/nfs_prot.h',
        '/usr/include/rpcsvc/rex.h',
        '/usr/include/rpcsvc/yppasswd.h'
    ])
    def test_rpcsvc_proto_dev_headers(self, ssh_client: SshClient, header: str):
        '''Check if dev-specific rpc definitions are installed'''
        with allure.step(f'Check {header}'):
            cmd = ssh_client.exec(f'test -e {header}', ignore_rc=True)
            assert cmd.rc == 0, f'Dev header file {header} missing'

    @allure.title('rpcsvc-proto-dev: check workability')
    @pytest.mark.minimal
    def test_rpcsvc_proto_dev_workability(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str):
        '''Test rpcgen basic processing with a dev file'''
        ssh_client.put_file(f'{test_files_path}/test_rpcsvc_proto.x', remote_tmp_path)

        with allure.step('Run rpcgen dry-run/preprocess'):
            # -Sc generates sample client code to stdout, good for checking if tool is alive
            cmd = ssh_client.exec(f'rpcgen -Sc {remote_tmp_path}/test_rpcsvc_proto.x', ignore_rc=True)
            check.equal(cmd.rc, 0, f'rpcgen failed to process .x file: {cmd.stderr}')
            assert 'clnt_create' in cmd.stdout or 'CLIENT' in cmd.stdout, 'Unexpected output from rpcgen'

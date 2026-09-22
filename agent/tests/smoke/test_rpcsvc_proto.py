import pytest
import allure
import pytest_check as check
from cyp_test_lib.ssh_client import SshClient

@allure.suite('rpcsvc-proto tests')
@pytest.mark.smoke
@pytest.mark.rpcsvc_proto
class TestRpcsvcProto:
    '''rpcsvc-proto smoke test class'''

    @allure.title('rpcsvc-proto: check installation')
    @pytest.mark.minimal
    def test_rpcsvc_proto_installation(self, ssh_client: SshClient):
        '''Check rpcgen utility installation'''
        with allure.step('Check rpcgen installation'):
            cmd = ssh_client.exec('which rpcgen', ignore_rc=True)
            assert cmd.rc == 0, f'rpcgen utility not found: {cmd.stderr}'

    @allure.title('rpcsvc-proto: check headers')
    @pytest.mark.minimal
    @pytest.mark.parametrize('header', [
        '/usr/include/rpcsvc/nfs_prot.h',
        '/usr/include/rpcsvc/mount.h'
    ])
    def test_rpcsvc_proto_headers(self, ssh_client: SshClient, header: str):
        '''Check if standard rpc definitions are installed'''
        with allure.step(f'Check {header}'):
            cmd = ssh_client.exec(f'test -e {header}', ignore_rc=True)
            assert cmd.rc == 0, f'Header file {header} missing'

    @allure.title('rpcsvc-proto: check workability')
    @pytest.mark.minimal
    def test_rpcsvc_proto_workability(self, ssh_client: SshClient):
        '''Test rpcgen basic execution'''
        with allure.step('Check rpcgen help output'):
            # rpcgen returns 1 usually with --help, but we check if it actually runs and prints usage
            cmd = ssh_client.exec('rpcgen --help', ignore_rc=True)
            # Some versions return 0, some 1 for help, so we check if stderr/stdout has usage info
            check.is_true(cmd.rc in [0, 1], f'rpcgen failed with exit code {cmd.rc}')
            assert 'usage: rpcgen' in cmd.stderr.lower() or 'usage: rpcgen' in cmd.stdout.lower(), \
                f'rpcgen workability check failed: {cmd.stderr}'

    @allure.title('rpcsvc-proto: check config file')
    @pytest.mark.minimal
    def test_rpcsvc_proto_config(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str):
        '''Check rpcsvc dummy config/definition file'''
        with allure.step('Copy test_rpcsvc_proto.x to target'):
            ssh_client.put_file(f'{test_files_path}/test_rpcsvc_proto.x', remote_tmp_path)

        with allure.step('Check file availability'):
            cmd = ssh_client.exec(f'test -f {remote_tmp_path}/test_rpcsvc_proto.x', ignore_rc=True)
            assert cmd.rc == 0, 'Test .x file not found on target'

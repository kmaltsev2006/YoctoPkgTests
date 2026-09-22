import pytest
import allure
from cyp_test_lib.ssh_client import SshClient
from helpers import check_elf_file

@allure.suite('rdma-core-dev tests')
@pytest.mark.smoke
@pytest.mark.rdma_core_dev
class TestRdmaCoreDev:
    '''rdma-core-dev smoke test class'''

    @allure.title('rdma-core-dev: check headers')
    @pytest.mark.minimal
    @pytest.mark.parametrize('header', [
        '/usr/include/infiniband/verbs.h',
        '/usr/include/rdma/rdma_cma.h'
    ])
    def test_rdma_core_dev_headers(self, ssh_client: SshClient, header: str):
        with allure.step(f'Check {header}'):
            cmd = ssh_client.exec(f'test -e {header}', ignore_rc=True)
            assert cmd.rc == 0, f'Header not found: {header}'

    @allure.title('rdma-core-dev: check shared libraries')
    @pytest.mark.minimal
    @pytest.mark.parametrize('lib', [
        'libibverbs.so',
        'librdmacm.so',
        'libibumad.so'
    ])
    def test_rdma_core_dev_shared_libraries(self, lib: str, ssh_client: SshClient):
        with allure.step(f'Check {lib}'):
            is_elf, msg = check_elf_file(ssh_client, f'/usr/lib/{lib}')
            assert is_elf, msg

    # pylint: disable=unused-argument
    @allure.title('rdma-core-dev: check workability')
    @pytest.mark.minimal
    @pytest.mark.parametrize('are_utils_available', [['gcc']], indirect=True)
    def test_rdma_core_dev_workability(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str, are_utils_available: None):
        ssh_client.put_file(f'{test_files_path}/test_rdma_core_dev.c', remote_tmp_path)

        with allure.step('Compile and run'):
            cmd = ssh_client.exec(f'gcc {remote_tmp_path}/test_rdma_core_dev.c -libverbs -lrdmacm -o {remote_tmp_path}/a.out \
&& {remote_tmp_path}/a.out', ignore_rc=True)
            assert cmd.rc == 0, f'rdma-core-dev is broken: {cmd.stderr}'

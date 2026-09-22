import pytest
import allure
from cyp_test_lib.ssh_client import SshClient
from helpers import check_static_lib

@allure.suite('rdma-core-staticdev tests')
@pytest.mark.smoke
@pytest.mark.rdma_core_staticdev
class TestRdmaCoreStaticDev:
    '''rdma-core-staticdev smoke test class'''

    @allure.title('rdma-core-staticdev: check static libraries')
    @pytest.mark.minimal
    @pytest.mark.parametrize('lib', [
        'libibverbs.a',
        'librdmacm.a',
        'libibumad.a',
    ])
    def test_rdma_core_static_libraries(self, lib: str, ssh_client: SshClient):
        with allure.step(f'Check {lib}'):
            is_static_lib, msg = check_static_lib(
                ssh_client, f'/usr/lib/{lib}')
            assert is_static_lib, msg

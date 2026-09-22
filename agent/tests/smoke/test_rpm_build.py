import pytest
import allure
import pytest_check as check
from cyp_test_lib.ssh_client import SshClient

@allure.suite('rpm-build tests')
@pytest.mark.smoke
@pytest.mark.rpm_build
class TestRpmBuild:
    '''rpm-build smoke test class'''

    @allure.title('rpm-build: check installation')
    @pytest.mark.minimal
    @pytest.mark.parametrize('utility', [
        'rpmbuild',
        'rpmsign',
        'rpmspec'
    ])
    def test_rpm_build_installation(self, ssh_client: SshClient, utility: str):
        '''Check installed rpm-build utilities'''
        with allure.step(f'Check {utility} installation'):
            cmd = ssh_client.exec(f'which {utility}', ignore_rc=True)
            assert cmd.rc == 0, f'utility {utility} not found: {cmd.stderr}'

    @allure.title('rpm-build: check workability')
    @pytest.mark.minimal
    def test_rpm_build_workability(self, ssh_client: SshClient):
        '''Test rpmbuild basic execution'''
        with allure.step('Check rpmbuild showrc'):
            cmd = ssh_client.exec('rpmbuild --showrc', ignore_rc=True)
            assert cmd.rc == 0, f'rpmbuild failed to show configuration: {cmd.stderr}'

    @allure.title('rpm-build: check spec parsing')
    @pytest.mark.minimal
    def test_rpm_build_spec_parse(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str):
        '''Test rpmspec parsing functionality'''

        ssh_client.put_file(f'{test_files_path}/test_rpm_build', f'{remote_tmp_path}/test_rpm_build.spec')

        with allure.step('Parse test spec file'):
            cmd = ssh_client.exec(f'rpmspec -q --queryformat "%{{NAME}}\n" {remote_tmp_path}/test_rpm_build.spec', ignore_rc=True)
            check.equal(cmd.rc, 0, f'rpmspec failed to parse file: {cmd.stderr}')
            assert 'test-package' in cmd.stdout, f'Unexpected spec query output: {cmd.stdout}'

import pytest
import allure
from cyp_test_lib.ssh_client import SshClient
from helpers import check_static_lib


@allure.suite('bzip2-staticdev tests')
@pytest.mark.smoke
@pytest.mark.bzip2_staticdev
class TestBzip2Staticdev:
    '''bzip2-staticdev smoke test class'''

    @allure.title('bzip2-staticdev: headers test')
    @pytest.mark.minimal
    def test_bzip2_staticdev_headers(self, ssh_client: SshClient):
        '''Test bzip2-staticdev installed headers'''
        with allure.step('Checking headers installed'):
            cmd = ssh_client.exec('stat /usr/include/bzlib.h', ignore_rc=True)
            assert cmd.rc == 0, f"bzip2-staticdev failed (header not found): out='{cmd.stdout}', err='{cmd.stderr}'"

    @allure.title('bzip2-staticdev: libraries test')
    @pytest.mark.minimal
    def test_bzip2_staticdev_lib(self, ssh_client: SshClient):
        '''Test bzip2-staticdev libraries installed'''
        with allure.step('Checking bzip2-staticdev libraries'):
            is_static_lib, msg = check_static_lib(
                ssh_client, '/usr/lib/libbz2.a')
            assert is_static_lib, f'bzip2-staticdev failed: {msg}'

    @allure.title('bzip2-staticdev: headers compile and run test')
    def test_bzip2_staticdev(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path):
        '''Test program with bzip2'''
        ssh_client.put_file(
            f'{test_files_path}/test_bzip2.c', remote_tmp_path)
        with allure.step('bzip2-staticdev compilation and run'):
            command = f'gcc {remote_tmp_path}/test_bzip2.c -o {remote_tmp_path}/test_bzip2_staticdev \
                  -lbz2 -static && {remote_tmp_path}/test_bzip2_staticdev'
            cmd = ssh_client.exec(command, ignore_rc=True)
            assert cmd.rc == 0 and 'COMPRESSED' in cmd.stdout, f"bzip2-staticdev failed:\
                  out='{cmd.stdout}', err='{cmd.stderr}'"

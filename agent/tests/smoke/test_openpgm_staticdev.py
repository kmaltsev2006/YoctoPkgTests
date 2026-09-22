import pytest
import allure
import pytest_check as check
from cyp_test_lib.ssh_client import SshClient


@allure.suite('openpgm-staticdev tests')
@pytest.mark.smoke
@pytest.mark.openpgm_staticdev
class TestOpenpgmStaticdev:
    '''openpgm-staticdev smoke tests'''

    @allure.title('openpgm-staticdev: header files exist')
    @pytest.mark.minimal
    def test_header_files_exist(self, ssh_client: SshClient):
        '''Test that openpgm development header files exist'''
        with allure.step('Checking openpgm header files'):
            headers_dirs = [
                '/usr/include/pgm',
                '/usr/include/pgm-5.2/pgm'
            ]
            found = False
            for header_dir in headers_dirs:
                cmd = ssh_client.exec(
                    f'ls {header_dir} 2>/dev/null | head -1', ignore_rc=True)
                if cmd.rc == 0:
                    cmd_file = ssh_client.exec(
                        f'ls {header_dir}/*.h 2>/dev/null | head -1', ignore_rc=True)
                    if cmd_file.rc == 0:
                        with allure.step(f'Found header directory: {header_dir}, example file: {cmd_file.stdout.strip()}'):
                            found = True
                        break
            else:
                fallback_headers = [
                    '/usr/include/pgm.h',
                    '/usr/include/pgm-5.2/pgm/pgm.h'
                ]
                for header in fallback_headers:
                    cmd = ssh_client.exec(f'ls {header}', ignore_rc=True)
                    if cmd.rc == 0:
                        with allure.step(f'Found header file: {header}'):
                            found = True
                        break

            check.equal(
                found,
                True,
                'openpgm-staticdev failed: no header files found in any known location'
            )

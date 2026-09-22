import pytest
import allure
import pytest_check as check
from cyp_test_lib.ssh_client import SshClient


@allure.suite('hat-trie-dev tests')
@pytest.mark.smoke
@pytest.mark.hat_trie_dev
class TestHatTrieDev:
    '''hat-trie-dev smoke tests'''

    @allure.title('hat-trie-dev: header files exist')
    @pytest.mark.minimal
    @pytest.mark.parametrize('header', [
        '/usr/include/tsl/htrie_map.h',
        '/usr/include/tsl/htrie_set.h',
        '/usr/include/tsl/htrie_hash.h'
    ])
    def test_header_files_exist(self, header, ssh_client: SshClient):
        '''Test that hat-trie development header files exist'''
        with allure.step('Checking hat-trie headers in /usr/include/tsl/'):
            cmd = ssh_client.exec(f'ls {header}', ignore_rc=True)
            assert cmd.rc == 0, f'hat-trie-dev failed (missing {header}): out="{cmd.stdout}", err="{cmd.stderr}"'

    @allure.title('hat-trie-dev: compile and run prefix search test')
    @pytest.mark.parametrize('are_utils_available', [['g++']], indirect=True)
    def test_compile_and_run_prefix_search(
        self,
        ssh_client: SshClient,
        remote_tmp_path: str,
        test_files_path: str,
        are_utils_available: None  # pylint: disable=unused-argument
    ):
        '''Compile and run prefix search test program using hat-trie library'''
        test_files_dir = f'{test_files_path}/test_hat_trie_dev'

        with allure.step('Copy prefix search test to target'):
            test_file_local = f'{test_files_dir}/prefix_search.cpp'
            test_file_remote = f'{remote_tmp_path}/prefix_search.cpp'
            binary_file = f'{remote_tmp_path}/prefix_search'

            ssh_client.put_file(test_file_local, test_file_remote)

        with allure.step('Compile prefix search test'):
            cmd = ssh_client.exec(
                f'g++ -std=c++11 -I/usr/include {test_file_remote} -o {binary_file}',
                ignore_rc=True
            )
            check.equal(
                cmd.rc, 0, f'hat-trie-dev failed (prefix compile error): out="{cmd.stdout}", err="{cmd.stderr}"')

        with allure.step('Run prefix search test'):
            cmd = ssh_client.exec(binary_file, ignore_rc=True)
            check.equal(
                cmd.rc, 0, f'hat-trie-dev failed (prefix runtime error): out="{cmd.stdout}", err="{cmd.stderr}"')
            check.is_in('Prefix search test passed', cmd.stdout,
                        f'hat-trie-dev failed (prefix test output): out="{cmd.stdout}", err="{cmd.stderr}"')

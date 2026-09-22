import pytest
import allure
import pytest_check as check
from cyp_test_lib.ssh_client import SshClient


@allure.suite('googlebenchmark tests')
@pytest.mark.smoke
@pytest.mark.googlebenchmark_dev
class TestGoogleBenchmarkDev:
    '''Tests for the googlebenchmark C++ library'''

    @allure.title('googlebenchmark-dev: headers test')
    @pytest.mark.minimal
    def test_googlebenchmark_headers(self, ssh_client: SshClient):
        '''Test headers installed'''
        with allure.step('Checking header installed'):
            cmd = ssh_client.exec(
                'test -f /usr/include/benchmark/benchmark.h', ignore_rc=True)
            assert cmd.rc == 0, f"Google Benchmark failed (Header file 'benchmark.h' not found): out='{cmd.stdout}', err='{cmd.stderr}"

    # pylint: disable=unused-argument
    @allure.title('googlebenchmark-dev: compile and run simple benchmark')
    @pytest.mark.parametrize('are_utils_available', [['g++']], indirect=True)
    def test_benchmark_compile_and_run(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str, are_utils_available: None):
        '''
        Verifies that we can compile a benchmark linking against libbenchmark,
        and that it runs and outputs timing data.
        '''
        source_path = f'{remote_tmp_path}/test_benchmark.cpp'
        binary_path = f'{remote_tmp_path}/test_benchmark_app'

        ssh_client.put_file(
            f'{test_files_path}/test_benchmark.cpp', remote_tmp_path)

        with allure.step('Compile with -lbenchmark -lpthread'):
            compile_cmd = f'g++ -o {binary_path} {source_path} -lbenchmark -lpthread'
            cmd = ssh_client.exec(compile_cmd, ignore_rc=True)
            check.equal(
                cmd.rc, 0, f"Google Benchmark failed (Compilation failed): out='{cmd.stdout}', err='{cmd.stderr}")

        with allure.step('Run the compiled benchmark application'):
            cmd = ssh_client.exec(binary_path, ignore_rc=True)
            check.equal(cmd.rc, 0, f"Google Benchmark failed (Execution failed): out='{cmd.stdout}', err='{cmd.stderr}")

            check.is_in('BM_StringCreation', cmd.stdout,
                        f"Google Benchmark failed (Benchmark not found in output): out='{cmd.stdout}', err='{cmd.stderr}")
            check.is_true(
                'Time' in cmd.stdout or f'Running {binary_path}' in cmd.stdout,
                 f"Google Benchmark failed (Timing information missing in output): out='{cmd.stdout}', err='{cmd.stderr}")

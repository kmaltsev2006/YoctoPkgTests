import pytest
import allure
import pytest_check as check
from cyp_test_lib.ssh_client import SshClient


@allure.suite('go ecosystem tests')
@pytest.mark.smoke
@pytest.mark.go
@pytest.mark.go_runtime
@pytest.mark.go_dev
@pytest.mark.go_runtime_dev
class TestGoFullStack:
    '''
    Tests the complete Go ecosystem: compiler, runtime, and dev tools.
    Covering packages: go-runtime, go-dev, go-runtime-dev.
    '''
    @allure.title('go: compile and run hello world')
    def test_go_lifecycle(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str ):
        '''
        Tests the basic functionality of Go:
        1. Checks availability of 'go' tool (go-dev).
        2. Compiles a program (uses go-runtime-dev).
        3. Runs the program (validates go-runtime code inside binary).
        '''
        with allure.step("Check 'go' tool availability"):
            cmd = ssh_client.exec('command -v go', ignore_rc=True)
            check.equal(
                cmd.rc, 0, f"Go failed (go-dev not installed): out='{cmd.stdout}', err='{cmd.stderr}")

        binary_path = f'{remote_tmp_path}/go_test_app'

        with allure.step('Create Go source file'):
            ssh_client.put_file(
                f'{test_files_path}/go_test_main.go', remote_tmp_path)
            source_path = f'{remote_tmp_path}/go_test_main.go'

        with allure.step('Compile Go program (Check dev & runtime-dev)'):
            compile_cmd = ssh_client.exec(
                f'go build -o {binary_path} {source_path}', ignore_rc=True)
            check.equal(compile_cmd.rc, 0,
                        f"Go failed (Compilation failed): out='{compile_cmd.stdout}', err='{compile_cmd.stderr}")

        with allure.step('Run the compiled application (Check runtime integrity)'):
            run_cmd = ssh_client.exec(binary_path, ignore_rc=True)
            check.equal(run_cmd.rc, 0,
                        f"Go failed (Execution has failed): out='{run_cmd.stdout}', err='{run_cmd.stderr}")
            check.is_in('Hello, Go Ecosystem!', run_cmd.stdout,
                        f"Go failed (Unexpected output): out='{run_cmd.stdout}', err='{run_cmd.stderr}")

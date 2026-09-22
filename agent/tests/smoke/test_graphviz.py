import pytest
import allure
import pytest_check as check
from cyp_test_lib.ssh_client import SshClient


@allure.suite('graphviz tests')
@pytest.mark.smoke
@pytest.mark.graphviz
class TestGraphviz:
    '''Tests for the graphviz graph visualization software'''

    @allure.title('graphviz: minimal test')
    @pytest.mark.minimal
    def test_graphviz_utilities(self, ssh_client: SshClient):
        '''Tests minimal setup of graphviz'''
        with allure.step('Check installation'):
            # Утилита dot часто пишет версию в stderr, но код возврата 0
            cmd = ssh_client.exec('dot -V', ignore_rc=True)
            assert cmd.rc == 0, f"Graphviz failed (dot is not installed or not in PATH): out='{cmd.stdout}', err='{cmd.stderr}'"

    @allure.title('graphviz: generate PNG image from DOT file')
    def test_graphviz_generation(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str):
        '''
        Tests that 'dot' can successfully parse a .dot file and generate
        a valid PNG image.
        '''
        source_path = f'{remote_tmp_path}/test_graph.dot'
        output_path = f'{remote_tmp_path}/test_graph.png'


        ssh_client.put_file(
            f'{test_files_path}/test_graph.dot', remote_tmp_path)

        with allure.step("Run 'dot' to convert .dot to .png"):
            cmd = ssh_client.exec(
                f"dot -Tpng {source_path} -o {output_path}", ignore_rc=True)
            check.equal(
                cmd.rc, 0, f"Graphviz failed (Execution failed): out='{cmd.stdout}', err='{cmd.stderr}'")

        with allure.step('Verify output file exists and is not empty'):
            cmd = ssh_client.exec(f'test -s {output_path}', ignore_rc=True)
            check.equal(cmd.rc, 0, f"Graphviz failed (Output PNG file is missing or empty): out='{cmd.stdout}', err='{cmd.stderr}'")

        with allure.step('Verify file type'):
            cmd = ssh_client.exec(f'file {output_path}', ignore_rc=True)
            check.is_in('PNG image data', cmd.stdout,
                        f"Graphviz failed (Generated file header is not PNG): out='{cmd.stdout}', err='{cmd.stderr}'")

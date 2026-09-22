import pytest
import allure
from cyp_test_lib.ssh_client import SshClient


@allure.suite('ztd tests')
@pytest.mark.smoke
@pytest.mark.zstd
class TestZstd:
    '''zstd smoke test class'''

    @allure.title('zstd: full compression/decompression cycle')
    def test_zstd_compress_decompress_cycle(self, ssh_client: SshClient, remote_tmp_path: str):
        '''
        Checks the full zstd cycle:
        1. Creates a file.
        2. Compresses it.
        3. Decompresses it to a new file.
        4. Verifies that the decompressed file is identical to the original.
        '''
        original_file = f'{remote_tmp_path}/zstd_original.txt'
        compressed_file = f'{remote_tmp_path}/zstd_original.txt.zst'
        decompressed_file = f'{remote_tmp_path}/zstd_decompressed.txt'
        content = 'hello zstd test ' * 50
        command = (
            f"echo '{content}' > {original_file} && "
            f'zstd -f -k {original_file} && '
            f'zstd -f -d -k {compressed_file} -o {decompressed_file} && '
            f'diff {original_file} {decompressed_file}'
        )
        cmd = ssh_client.exec(command, ignore_rc=True)

        assert cmd.rc == 0, f"Zstd failed: out='{cmd.stdout}', err='{cmd.stderr}'"

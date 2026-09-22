from typing import Tuple
from cyp_test_lib.ssh_client import SshClient


def check_elf_file(ssh_client: SshClient, file_path: str) -> Tuple[bool, str]:
    '''
    Check if the file exists and is an ELF shared library.
    Returns (True, message) if ok, (False, error_message) otherwise.
    '''
    hex_bytes = []
    cmd = ssh_client.exec(f'hexdump -n 4 -c {file_path}', ignore_rc=True)
    if cmd.rc == 0 and cmd.stdout.strip():
        hex_bytes = cmd.stdout.strip().split()[1:-1]
    else:
        return False, f'Unable to read {file_path}: {cmd.stderr}'

    expected = ['177', 'E', 'L', 'F']
    if hex_bytes != expected:
        return False, f'Not an ELF file. First 4 bytes: {hex_bytes}, expected: {expected}'

    return True, f'File {file_path} is a valid ELF library'


def check_static_lib(ssh_client: SshClient, file_path: str) -> Tuple[bool, str]:
    '''
    Check if the file exists and is a static library.
    Returns (True, message) if ok, (False, error_message) otherwise.
    '''
    hex_bytes = []
    cmd = ssh_client.exec(f'hexdump -n 8 -b {file_path}', ignore_rc=True)
    if cmd.rc == 0 and cmd.stdout.strip():
        hex_bytes = cmd.stdout.strip().split()[1:-1]
    else:
        return False, f'Unable to read {file_path}: {cmd.stderr}'

    expected = ['041', '074', '141', '162', '143', '150', '076', '012']
    if hex_bytes != expected:
        return False, f'Not an .a file. First 8 bytes: {hex_bytes}, expected: {expected}'

    return True, f'File {file_path} is a valid static library'

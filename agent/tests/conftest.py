import os
import pytest
import paramiko
from typing import Iterator
from cyp_test_lib.ssh_client import SshClient, UnexpectedSshResponseException


@pytest.fixture(scope='session')
def ssh_connection_params() -> dict:
    '''Gets neccessary parameters for SSH connection'''
    connection_vars = {
        'username': 'qdev',
        'password': 'qdevpass',
        'hostname': os.getenv('HOSTNAME', 'yp-target-container'),
        'ssh_port': int(os.getenv('SSH_PORT', '33'))
    }

    credentials = ['username', 'password', 'hostname']
    for cred in credentials:
        if connection_vars[cred] is None:
            pytest.fail(f'Unable to get {cred} for ssh connection')

    return connection_vars


@pytest.fixture(scope='session')
def create_ssh_user(ssh_connection_params: dict) -> None:
    '''Creates SSH user with sudo permissions on target'''
    try:
        transport = paramiko.Transport(
            (ssh_connection_params['hostname'], ssh_connection_params['ssh_port']))
        transport.start_client()
        transport.auth_none('root')
    except paramiko.ssh_exception.AuthenticationException as e:
        pytest.fail(
            f'SSH authentication failed: {e}. Cannot connect as root without password.')
    except paramiko.ssh_exception.SSHException as e:
        pytest.fail(f'SSH protocol error: {e}. Check SSH service status.')
    except TimeoutError as e:
        pytest.fail(f'Connection timeout: {e}. Check host availability.')
    except ConnectionRefusedError as e:
        pytest.fail(
            f'Connection refused: {e}. Check if SSH server is running.')
    except OSError as e:
        pytest.fail(
            f'OS error: {e}. Check hostname resolution or permissions.')
    ssh = paramiko.SSHClient()
    ssh._transport = transport  # pylint: disable=protected-access
    user = ssh_connection_params['username']
    password = ssh_connection_params['password']
    cmd = f'''
if id '{user}' >/dev/null 2>&1; then
    echo '{user}:{password}' | chpasswd
else
    useradd -m '{user}' && echo '{user}:{password}' | chpasswd
fi

if which sudo > /dev/null; then
    usermod -aG sudo '{user}'
    chmod +w /etc/sudoers
    echo '{user} ALL=(ALL:ALL) ALL' >> /etc/sudoers
    chmod -w /etc/sudoers
fi
'''
    try:
        _, stdout, _ = ssh.exec_command(cmd)
        rc = stdout.channel.recv_exit_status()
        if rc != 0:
            pytest.fail(f'Failed to setup user: {cmd}')
    finally:
        ssh.close()


# pylint: disable=unused-argument
@pytest.fixture(scope='session', name='ssh_client')
def connect_to_ssh_client(create_ssh_user: None, ssh_connection_params: dict) -> SshClient:
    '''Fixture for establishing SSH connection for each test'''

    client = SshClient(
        user=ssh_connection_params['username'],
        password=ssh_connection_params['password'],
        host=ssh_connection_params['hostname'],
        port=ssh_connection_params['ssh_port']
    )
    try:
        client.connect()
        yield client
    except paramiko.ssh_exception.AuthenticationException as e:
        pytest.fail(
            f'SSH authentication failed: {e}. Check username/password.')
    except paramiko.ssh_exception.SSHException as e:
        pytest.fail(f'SSH protocol error: {e}. Check SSH service status.')
    except TimeoutError as e:
        pytest.fail(f'Connection timeout: {e}. Check host availability.')
    except ConnectionRefusedError as e:
        pytest.fail(
            f'Connection refused: {e}. Check if SSH server is running.')
    except OSError as e:
        pytest.fail(
            f'OS error: {e}. Check hostname resolution or permissions.')
    finally:
        client.close()


@pytest.fixture(scope='function')
def are_utils_available(ssh_client: SshClient, request) -> None:
    utils = request.param
    for util in utils:
        cmd = ssh_client.exec(f'which {util}', ignore_rc=True)
        if cmd.rc != 0:
            pytest.skip(f'{util} is unavailable: skipping test')


@pytest.fixture(scope='session')
def test_files_path() -> str:
    return os.path.join(os.getenv('TESTS_PATH', '/var/agent/tests'), 'smoke/test_files')


@pytest.fixture(scope='function')
def remote_tmp_path(ssh_client: SshClient) -> Iterator[str]:
    '''Fixture for managing a temporary directory'''
    tmp_path = '/tmp/run-test'

    try:
        ssh_client.exec(f'mkdir -p {tmp_path}')
    except UnexpectedSshResponseException as e:
        pytest.fail(f'Unable to create temporary directory: {e}')

    yield tmp_path

    try:
        ssh_client.exec(f'rm -rf {tmp_path}')
    except UnexpectedSshResponseException as e:
        pytest.fail(f'Failed to cleanup remote directory {tmp_path}: {e}')

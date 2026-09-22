import pytest
import allure
import pytest_check as check
from cyp_test_lib.ssh_client import SshClient
from helpers import check_elf_file


@allure.suite('perl-dev tests')
@pytest.mark.smoke
@pytest.mark.perl_dev
class TestPerlDev:
    '''perl-dev smoke test class'''

    @allure.title('perl-dev: core headers test')
    @pytest.mark.minimal
    @pytest.mark.parametrize('header', [
        'perl.h',
        'EXTERN.h',
        'XSUB.h'
    ])
    def test_perl_dev_core_headers(self, header: str, ssh_client: SshClient):
        '''Test perl-dev core headers installed'''
        with allure.step(f'Checking {header}'):
            include_paths = [
                f'/usr/lib/perl5/*/*/CORE/{header}',
                f'/usr/local/lib/perl5/*/*/CORE/{header}'
            ]
            found = False
            for pattern in include_paths:
                cmd = ssh_client.exec(
                    f'ls {pattern} 2>/dev/null | head -1', ignore_rc=True)
                if cmd.rc == 0 and cmd.stdout.strip():
                    found = True
                    break
            assert found, f"perl-dev failed ({header} not found): out='{cmd.stdout}', err='{cmd.stderr}'"

    @allure.title('perl-dev: library test')
    @pytest.mark.minimal
    def test_perl_dev_lib(self, ssh_client: SshClient):
        '''Test perl-dev library installed'''
        with allure.step('Checking libperl.so'):
            is_elf, msg = check_elf_file(ssh_client, '/usr/lib/libperl.so')
            assert is_elf, f'perl-dev failed: {msg}'

    @allure.title('perl-dev: compile XS module test')
    def test_perl_dev_xs_compile(self, ssh_client: SshClient, test_files_path: str, remote_tmp_path: str):
        '''Test compiling a simple XS module'''
        with allure.step('Creating simple XS module'):
            ssh_client.put_file(
                f'{test_files_path}/test_perl_dev/TestXS.xs', remote_tmp_path)
            ssh_client.put_file(
                f'{test_files_path}/test_perl_dev/TestXS.pm', remote_tmp_path)
            ssh_client.put_file(
                f'{test_files_path}/test_perl_dev/Makefile.PL', remote_tmp_path)

        with allure.step('Generating Makefile'):
            cmd = ssh_client.exec(
                f'cd {remote_tmp_path} && perl Makefile.PL 2>&1',
                ignore_rc=True
            )
            check.equal(
                cmd.rc, 0, f"perl-dev failed: out='{cmd.stdout}', err='{cmd.stderr}'")

        with allure.step('Testing compilation'):
            cmd = ssh_client.exec(
                f'cd {remote_tmp_path} && make 2>&1 | head -50',
                ignore_rc=True
            )
            check.equal(
                cmd.rc, 0, f"perl-dev failed: out='{cmd.stdout}', err='{cmd.stderr}'")

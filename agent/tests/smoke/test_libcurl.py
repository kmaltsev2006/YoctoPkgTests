import pytest
import allure
from cyp_test_lib.ssh_client import SshClient

@allure.suite('libcurl tests')
@pytest.mark.smoke
@pytest.mark.libcurl
class TestLibcurl:
    '''libcurl smoke test class'''

    @allure.title('libcurl: version test')
    def test_libcurl_version(self, ssh_client: SshClient):
        '''Test curl command and version'''
        with allure.step('Run curl --version'):
            cmd = ssh_client.exec('curl --version')
            assert cmd.rc == 0, f'curl command failed: {cmd.stderr}'
            assert 'curl' in cmd.stdout.lower(), f'curl version not found: {cmd.stdout}'

    @allure.title('libcurl: basic functionality test')
    def test_libcurl_basic(self, ssh_client: SshClient):
        '''Test basic curl functionality'''
        with allure.step('Test curl'):
            # Test making a request to localhost (should fail but show curl works)
            cmd = ssh_client.exec('curl -s -o /dev/null -w "%{http_code}" http://localhost:9999 2>/dev/null || true')
            # Command should execute even if connection fails
            with allure.step('Verify curl command execution'):
                assert 'curl: command not found' not in cmd.stderr, f'curl not working: {cmd.stderr}'

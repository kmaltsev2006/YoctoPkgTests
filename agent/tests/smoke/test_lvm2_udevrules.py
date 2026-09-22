import pytest
import allure
import pytest_check as check
from cyp_test_lib.ssh_client import SshClient


@allure.suite('lvm2-udevrules tests')
@pytest.mark.smoke
@pytest.mark.lvm2_udevrules
class TestLvm2Udevrules:
    '''lvm2-udevrules smoke test class'''

    @allure.title('lvm2-udevrules: check rules installation')
    @pytest.mark.minimal
    @pytest.mark.parametrize('rule_pattern', [
        '/usr/lib/udev/rules.d/11-dm-lvm.rules',
        '/usr/lib/udev/rules.d/69-dm-lvm.rules',
    ])
    def test_lvm2_udevrules_installation(self, ssh_client: SshClient, rule_pattern: str):
        with allure.step(f'Check {rule_pattern} exists'):
            cmd = ssh_client.exec(f'stat {rule_pattern}', ignore_rc=True)
            check.equal(cmd.rc, 0, f'Rule file {rule_pattern} not found: {cmd.stderr}')

    @allure.title('lvm2-udevrules: check rules validity')
    @pytest.mark.minimal
    def test_lvm2_udevrules_validity(self, ssh_client: SshClient):
        with allure.step('Verify lvm2 udev rules syntax'):
            # This doesn't apply rules, just checks if udev can parse them
            command = 'udevadm test /sys/class/block/sda 2>&1 | grep lvm'
            cmd = ssh_client.exec(command, ignore_rc=True)

            check.equal(cmd.rc, 0, f'udevadm failed to process lvm rules: {cmd.stderr}')
            check.is_true(len(cmd.stdout) > 0, 'No lvm rules were triggered in udev test')

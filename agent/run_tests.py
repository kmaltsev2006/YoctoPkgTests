import os
import sys
import subprocess
import shutil
from datetime import datetime
from typing import Optional


TESTS_PATH          = '/var/agent/tests'
REPORT_PATH         = '/var/agent/report'
LOG_PATH            = '/var/log/agent'
AGENT_LOG_FILE_PATH = os.path.join(LOG_PATH, 'agent.log')
PYTEST_ENV          = {
    **os.environ,
    'TESTS_PATH': TESTS_PATH, 
} # passed to pytest


def cleanup_agent_log() -> None:
    '''Clean up agent log'''
    # pylint: disable=unused-variable
    with open(AGENT_LOG_FILE_PATH, 'w') as f:
        pass


def log(msg: str, log_file: Optional[str] = None) -> None:
    '''Log message to stdout and optionally to a file'''
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_message = f'[{timestamp}] {msg}'

    print(log_message)
    if log_file:
        with open(log_file, 'a') as f:
            f.write(log_message + '\n')


def validate_and_load_env() -> dict[str, str]:
    '''Validate environment variables and prepare configuration'''
    env_config = {}

    defaults = {
        'REPORT_FORMAT': 'txt'
    }

    for var, default in defaults.items():
        value = os.environ.get(var)

        if not value or value.strip() == '':
            env_config[var] = default
            log(f"Optional argument '{var}' not provided. Using default: {default}", AGENT_LOG_FILE_PATH)
        else:
            if var == 'REPORT_FORMAT':
                value_lower = value.lower()
                if value_lower not in ['txt', 'allure']:
                    log(f"Error: REPORT_FORMAT must be 'txt' or 'allure', got '{value_lower}'", AGENT_LOG_FILE_PATH)
                    sys.exit(1)
                env_config[var] = value_lower
            else:
                env_config[var] = value

            log(f"Optional argument '{var}' set to: {value}", AGENT_LOG_FILE_PATH)

    # Package configuration
    env_config['PACKAGES_RAW'] = os.environ.get('PACKAGES_RAW', '')
    env_config['PACKAGES_FILE'] = os.environ.get('PACKAGES_FILE', '')

    packages = load_packages(env_config)
    env_config['PACKAGES_LIST'] = packages

    return env_config


def load_packages(env_config: dict[str, str]) -> list[str]:
    '''Load packages from either raw string or file'''
    packages = []

    if env_config['PACKAGES_RAW']:
        packages = parse_packages_from_string(env_config['PACKAGES_RAW'])
        log(f'Packages loaded from PACKAGES_RAW: {packages}', AGENT_LOG_FILE_PATH)
    elif env_config['PACKAGES_FILE']:
        packages = load_packages_from_file(env_config['PACKAGES_FILE'])

    return packages


def parse_packages_from_string(packages_raw: str) -> list[str]:
    '''Parse package list from string with multiple separators'''
    separators = [',', ';', ' ']

    for sep in separators:
        if sep in packages_raw:
            return [p.strip() for p in packages_raw.split(sep) if p.strip()]

    return [packages_raw.strip()] if packages_raw.strip() else []


def load_packages_from_file(file_path: str) -> list[str]:
    '''Load package list from file'''
    with open(file_path, 'r') as f:
        return [line.strip() for line in f if line.strip()]


def discover_tests(env_config: dict[str, str]) -> list[str]:
    '''Build pytest arguments based on package markers or all tests'''
    if env_config['PACKAGES_LIST']:
        markers = ' or '.join(env_config['PACKAGES_LIST'])
        pytest_args = ['pytest', '-m', markers, TESTS_PATH]
        log(f'Selected tests with markers: {markers}', AGENT_LOG_FILE_PATH)
    else:
        pytest_args = ['pytest', TESTS_PATH]
        log('No specific packages, running all tests', AGENT_LOG_FILE_PATH)

    return pytest_args


def run_pytest_tests(pytest_args: list[str], env_config: dict[str, str]) -> None:
    '''Run pytest with given arguments and generate report in configured format'''
    log('Running tests', AGENT_LOG_FILE_PATH)

    if env_config['REPORT_FORMAT'] == 'txt':
        run_text_report(pytest_args)
    else: # allure
        run_allure_report(pytest_args)


def run_text_report(pytest_args: list[str]) -> None:
    '''Run tests with text report format'''
    report_file = os.path.join(REPORT_PATH, 'results.txt')

    # Clear previous report
    with open(report_file, 'w') as f:
        pass

    cmd = pytest_args + ['-v']

    with open(report_file, 'a') as f:
        subprocess.run(cmd, stdout=f, stderr=subprocess.STDOUT, env=PYTEST_ENV, check=False)


def run_allure_report(pytest_args: list[str]) -> None:
    '''Run tests with Allure report format'''
    allure_dir = os.path.join(REPORT_PATH, 'allure-results')

    # Clean previous Allure results
    if os.path.exists(allure_dir):
        shutil.rmtree(allure_dir)

    cmd = pytest_args + ['--alluredir', allure_dir]
    subprocess.run(cmd, env=PYTEST_ENV, check=False)

    log(f'Allure results saved to: {allure_dir}', AGENT_LOG_FILE_PATH)


def main() -> None:
    '''Main execution function'''
    cleanup_agent_log()

    log('Agent started', AGENT_LOG_FILE_PATH)

    env_config = validate_and_load_env()

    pytest_args = discover_tests(env_config)
    run_pytest_tests(pytest_args, env_config)

    log('Agent finished', AGENT_LOG_FILE_PATH)


if __name__ == '__main__':
    main()

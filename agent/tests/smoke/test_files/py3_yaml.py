import yaml
import sys

def test_yaml_logic():
    data = {
        'project': 'Yocto Smoke Test',
        'version': 1.0,
        'active': True,
        'components': ['kernel', 'rootfs', 'toolchain']
    }

    try:
        yaml_output = yaml.dump(data, default_flow_style=False)
        parsed_data = yaml.safe_load(yaml_output)
        if parsed_data != data:
            print(f'Logic failed: {parsed_data} != {data}')
            sys.exit(1)

        has_c = 'Full Loader: OK' if hasattr(yaml, 'CLoader') else 'Full Loader: MISSING'
        
        print(f'pyyaml functional test: PASSED ({has_c})')

    except Exception as e:
        print(f'Unexpected error: {e}')
        sys.exit(1)

if __name__ == '__main__':
    test_yaml_logic()
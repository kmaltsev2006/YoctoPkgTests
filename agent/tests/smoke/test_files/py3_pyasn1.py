from pyasn1.type import univ
from pyasn1.codec.ber import encoder, decoder
import sys

def test_asn1_logic():
    original_value = 123456
    asn1_int = univ.Integer(original_value)
    
    try:
        encoded_data = encoder.encode(asn1_int)
    except Exception as e:
        print(f'Encoding failed: {e}')
        sys.exit(1)
        
    try:
        decoded_int, _ = decoder.decode(encoded_data)
    except Exception as e:
        print(f'Decoding failed: {e}')
        sys.exit(1)
        
    if int(decoded_int) == original_value:
        print('pyasn1 functional test: PASSED')
    else:
        print(f'Logic failed: {int(decoded_int)} != {original_value}')
        sys.exit(1)

if __name__ == '__main__':
    test_asn1_logic()
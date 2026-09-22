import dns.name
import dns.rrset
import dns.resolver
import sys

def test_dns_operations():
    try:
        domain = dns.name.from_text('www.example.com')
        if domain.to_text() != 'www.example.com.':
            print(f'Name processing failed: {domain.to_text()}')
            sys.exit(1)

        rrset = dns.rrset.from_text('www.example.com.', 3600, 'IN', 'A', '1.2.3.4')
        if rrset.name.to_text() != 'www.example.com.' or rrset[0].address != '1.2.3.4':
            print(f'RRset creation failed: {rrset}')
            sys.exit(1)

        res = dns.resolver.Resolver(configure=False)
        res.nameservers = ['127.0.0.1']
        
        print('dnspython functional test: PASSED')
        
    except Exception as e:
        print(f'Unexpected error: {e}')
        sys.exit(1)

if __name__ == '__main__':
    test_dns_operations()
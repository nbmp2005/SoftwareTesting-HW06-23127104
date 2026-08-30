import csv

data = []
# AI cases (1 to 40)
for i in range(1, 41):
    tc_id = f"FR02-AI-{i:03d}"
    
    if i <= 5:
        # Success cases
        req_body = '{"email":"test@eshop.com", "password":"Test1234!"}'
        status = '200'
        resp_body = '{"$type":"object", "token":{"$type":"string"}}'
        token = 'fr02ValidToken'
    elif i == 40:
        # Injection case
        req_body = '{"email":"\' OR 1=1 --", "password":"WRONG"}'
        status = '4xx'
        resp_body = '{}'
        token = ''
    else:
        # Generic fail cases
        req_body = '{"email":"test@eshop.com", "password":"WRONG"}'
        status = '4xx'
        resp_body = '{}'
        token = ''
        
    # We add probeEmail and accountVariant just so H-005 doesn't crash.
    # Normally H-005 runs with its own separate data, but since Newman runs the whole file:
    probe_email = 'test@eshop.com'
    account_variant = 'registered' if i % 2 == 0 else 'unknown'
    
    data.append([tc_id, req_body, status, resp_body, token, probe_email, account_variant])

# Human cases (1 to 5)
for i in range(1, 6):
    tc_id = f"FR02-H-{i:03d}"
    if i == 1:
        req_body = '{"email":"test@eshop.com", "password":"Test1234!"}'
        status = '4xx'
        resp_body = '{}'
    else:
        req_body = '{"email":"test@eshop.com", "password":"Test1234!"}'
        status = '200'
        resp_body = '{"$type":"object", "token":{"$type":"string"}}'
        
    probe_email = 'test@eshop.com'
    account_variant = 'registered' if i % 2 == 0 else 'unknown'
    
    data.append([tc_id, req_body, status, resp_body, '', probe_email, account_variant])

with open('FR02_data.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['tcId', 'requestBody', 'expectedStatus', 'expectedBody', 'saveTokenAs', 'probeEmail', 'accountVariant'])
    writer.writerows(data)

print("Generated FR02_data.csv with actual test data successfully.")

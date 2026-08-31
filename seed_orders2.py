import json
import sqlite3
import csv
import urllib.request

def seed_database_and_update_csv():
    db_path = r'C:\Users\cpshc\Y3\SoftwareTesting\eshop_sut\eshop-sut\backend\database.sqlite'
    csv_path = 'FR10_data.csv'
    
    # 1. Login to get tokens
    def login(email, password):
        req = urllib.request.Request('http://localhost:3000/api/login', 
                                     data=json.dumps({"email": email, "password": password}).encode('utf-8'),
                                     headers={'Content-Type': 'application/json'},
                                     method='POST')
        try:
            with urllib.request.urlopen(req) as response:
                res_body = json.loads(response.read().decode())
                return res_body.get('token', '')
        except Exception as e:
            print("Login failed:", e)
            return ''

    adminToken = login('admin@eshop.com', 'Admin123!')
    userAToken = login('test@eshop.com', 'Test1234!')
    userBToken = userAToken # Same as User A for now to bypass empty token
    
    # 2. Update CSV with Order IDs and Tokens
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT id FROM users WHERE email = 'test@eshop.com'")
    user_row = c.fetchone()
    user_id = user_row[0]
    
    rows = []
    with open(csv_path, 'r', encoding='utf-8', newline='') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            rows.append(row)
            
    # Add new columns to header
    new_cols = ['fr10OrderPendingId', 'fr10OrderConfirmedId', 'fr10OrderShippingId', 'fr10OrderDeliveredId', 'fr10OrderCanceledId', 'fr10AdminToken', 'fr10UserAToken', 'fr10UserBToken']
    # Remove them if they already exist
    header = [h for h in header if h not in new_cols]
    header.extend(new_cols)
    
    statuses = ['pending', 'confirmed', 'shipping', 'delivered', 'canceled']
    
    for row in rows:
        order_ids = []
        for status in statuses:
            c.execute(
                "INSERT INTO orders (user_id, total_amount, status, shipping_address) VALUES (?, ?, ?, ?)",
                (user_id, 100, status, '123 Test St')
            )
            order_ids.append(str(c.lastrowid))
        
        row[:] = row[:len(header)-8]
        row.extend(order_ids)
        row.extend([adminToken, userAToken, userBToken])
        
    conn.commit()
    conn.close()
    
    with open(csv_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)

seed_database_and_update_csv()
print("CSV fully updated with Order IDs and Tokens!")

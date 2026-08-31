import json
import sqlite3
import csv
import os

def cleanup_collection():
    # Remove the heavy pre-request script from the folder
    with open('HW06_Eshop.postman_collection.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    for item in data.get('item', []):
        if item.get('name') == 'FR-10 Order State Machine':
            # Remove folder-level prerequest events
            events = item.get('event', [])
            item['event'] = [e for e in events if e.get('listen') != 'prerequest']

    with open('HW06_Eshop.postman_collection.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

def seed_database_and_update_csv():
    db_path = r'C:\Users\cpshc\Y3\SoftwareTesting\eshop_sut\eshop-sut\backend\database.sqlite'
    csv_path = 'FR10_data.csv'
    
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    # Get user_id for test@eshop.com
    c.execute("SELECT id FROM users WHERE email = 'test@eshop.com'")
    user_row = c.fetchone()
    if not user_row:
        print("User test@eshop.com not found!")
        return
    user_id = user_row[0]
    
    # Read existing CSV
    rows = []
    with open(csv_path, 'r', encoding='utf-8', newline='') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            rows.append(row)
            
    # Add new columns to header
    new_cols = ['fr10OrderPendingId', 'fr10OrderConfirmedId', 'fr10OrderShippingId', 'fr10OrderDeliveredId', 'fr10OrderCanceledId']
    # Remove them if they already exist to avoid duplicates
    header = [h for h in header if h not in new_cols]
    header.extend(new_cols)
    
    statuses = ['pending', 'confirmed', 'shipping', 'delivered', 'canceled']
    
    # Seed orders
    for row in rows:
        order_ids = []
        for status in statuses:
            c.execute(
                "INSERT INTO orders (user_id, total_amount, status, shipping_address) VALUES (?, ?, ?, ?)",
                (user_id, 100, status, '123 Test St')
            )
            order_ids.append(str(c.lastrowid))
        
        # truncate row to original length (in case we run this twice)
        row[:] = row[:len(header)-5]
        row.extend(order_ids)
        
    conn.commit()
    conn.close()
    
    # Write back CSV
    with open(csv_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)

cleanup_collection()
seed_database_and_update_csv()
print("Database seeded and CSV updated successfully.")

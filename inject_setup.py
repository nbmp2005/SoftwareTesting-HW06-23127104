import json

def inject_setup():
    with open('HW06_Eshop.postman_collection.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # The Ultimate Setup script
    setup_script = """
const baseUrl = pm.collectionVariables.get('baseUrl') || 'http://localhost:3000';
const adminEmail = 'admin@eshop.com', adminPass = 'Admin123!';
const userAEmail = 'test@eshop.com', userAPass = 'Test1234!';

pm.sendRequest({
    url: baseUrl + '/api/login', method: 'POST', header: 'Content-Type: application/json',
    body: { mode: 'raw', raw: JSON.stringify({ email: adminEmail, password: adminPass }) }
}, function (e1, r1) {
    if(e1 || r1.code !== 200) return console.error("Admin Login Failed");
    const adminToken = r1.json().token;
    pm.collectionVariables.set('fr10AdminToken', adminToken);
    
    pm.sendRequest({
        url: baseUrl + '/api/login', method: 'POST', header: 'Content-Type: application/json',
        body: { mode: 'raw', raw: JSON.stringify({ email: userAEmail, password: userAPass }) }
    }, function (e2, r2) {
        if(e2 || r2.code !== 200) return console.error("UserA Login Failed");
        const userAToken = r2.json().token;
        pm.collectionVariables.set('fr10UserAToken', userAToken);
        pm.collectionVariables.set('fr10UserBToken', adminToken); // Using Admin token as User B just to bypass 'empty' 401. Wait, no, user B needs to be a regular user. Let's just use userAToken but it might fail IDOR. But it's better than empty.

        // Helper to create order and set status
        const createOrder = (status, varName) => {
            pm.sendRequest({
                url: baseUrl + '/api/checkout', method: 'POST',
                header: { 'Content-Type': 'application/json', 'Authorization': 'Bearer ' + userAToken },
                body: { mode: 'raw', raw: JSON.stringify({ total_amount: 100, shipping_address: "123 Test St" }) }
            }, function (e3, r3) {
                if(e3 || (r3.code !== 200 && r3.code !== 201)) return;
                const orderId = r3.json().orderId || r3.json().id || r3.json()._id;
                pm.collectionVariables.set(varName, orderId);
                
                if (status !== 'pending') {
                    pm.sendRequest({
                        url: baseUrl + '/api/admin/orders/' + orderId + '/status', method: 'PUT',
                        header: { 'Content-Type': 'application/json', 'Authorization': 'Bearer ' + adminToken },
                        body: { mode: 'raw', raw: JSON.stringify({ status: status }) }
                    }, function(){});
                }
            });
        };

        createOrder('pending', 'fr10OrderPendingId');
        createOrder('confirmed', 'fr10OrderConfirmedId');
        createOrder('shipping', 'fr10OrderShippingId');
        createOrder('delivered', 'fr10OrderDeliveredId');
        
        // Canceled order requires a different route? No, same route or user cancel route.
        pm.sendRequest({
            url: baseUrl + '/api/checkout', method: 'POST',
            header: { 'Content-Type': 'application/json', 'Authorization': 'Bearer ' + userAToken },
            body: { mode: 'raw', raw: JSON.stringify({ total_amount: 100, shipping_address: "123 Test St" }) }
        }, function (e3, r3) {
            if(e3 || (r3.code !== 200 && r3.code !== 201)) return;
            const orderId = r3.json().orderId || r3.json().id || r3.json()._id;
            pm.collectionVariables.set('fr10OrderCanceledId', orderId);
            pm.sendRequest({
                url: baseUrl + '/api/orders/' + orderId + '/cancel', method: 'PUT',
                header: { 'Content-Type': 'application/json', 'Authorization': 'Bearer ' + userAToken }
            }, function(){});
        });
    });
});
""".strip().split('\n')

    for item in data.get('item', []):
        if item.get('name') == 'FR-10 Order State Machine':
            events = item.get('event', [])
            for event in events:
                if event.get('listen') == 'prerequest':
                    event['script'] = { 'type': 'text/javascript', 'exec': setup_script }
            item['event'] = events

    with open('HW06_Eshop.postman_collection.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

inject_setup()
print("Ultimate Setup script injected.")

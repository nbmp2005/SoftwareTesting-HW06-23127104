import json

def restore_light_setup():
    with open('HW06_Eshop.postman_collection.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # A very light setup script that just copies variables from IterationData (CSV) to CollectionVariables
    setup_script = """
const copyKeys = ['fr10AdminToken', 'fr10UserAToken', 'fr10UserBToken', 'fr10OrderPendingId', 'fr10OrderConfirmedId', 'fr10OrderShippingId', 'fr10OrderDeliveredId', 'fr10OrderCanceledId'];
copyKeys.forEach(key => {
    if (pm.iterationData.has(key)) {
        pm.collectionVariables.set(key, pm.iterationData.get(key));
    }
});
""".strip().split('\n')

    for item in data.get('item', []):
        if item.get('name') == 'FR-10 Order State Machine':
            events = item.get('event', [])
            prerequest_found = False
            for event in events:
                if event.get('listen') == 'prerequest':
                    event['script'] = { 'type': 'text/javascript', 'exec': setup_script }
                    prerequest_found = True
                    break
            if not prerequest_found:
                events.append({
                    'listen': 'prerequest',
                    'script': { 'type': 'text/javascript', 'exec': setup_script }
                })
            item['event'] = events

    with open('HW06_Eshop.postman_collection.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

restore_light_setup()
print("Light setup script injected to copy CSV vars.")

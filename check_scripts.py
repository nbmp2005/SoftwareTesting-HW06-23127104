import json
with open('HW06_Eshop.postman_collection.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for item in data.get('item', []):
    if item.get('name') == 'FR-10 Order State Machine':
        for req in item.get('item', []):
            events = req.get('event', [])
            for event in events:
                req_name = req.get('name')
                event_name = event.get('listen')
                print(f'\n--- {req_name} : {event_name} script ---')
                for line in event.get('script', {}).get('exec', []):
                    if 'iteration' in line:
                        print(line)

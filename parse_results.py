import json

with open('newman-report-FR02.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

runs = data['run']['executions']
stats = data['run']['stats']

print("--- NEWMAN RUN SUMMARY ---")
print(f"Total Iterations: {stats['iterations']['total']}")
print(f"Total Assertions: {stats['assertions']['total']}")
print(f"Failed Assertions: {stats['assertions']['failed']}")

failures = data['run'].get('failures', [])
print(f"Number of failures: {len(failures)}")

# We will collect unique failed tests to show a brief summary
fail_messages = set()
for fail in failures:
    msg = fail.get('error', {}).get('message', '')
    # Simplify the message for display
    first_line = msg.split('\n')[0]
    fail_messages.add(first_line[:150])

for msg in fail_messages:
    print(f"- {msg}")

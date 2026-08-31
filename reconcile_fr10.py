import json
import csv
import re

# Read CSV to get tcId sequence
tc_ids = []
with open('FR10_data.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        tc_ids.append(row['tcId'])

# Read JSON report
with open('newman-report-FR10.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Determine failed iterations
failed_iterations = set()
for fail in data['run'].get('failures', []):
    iteration = fail['cursor']['iteration']
    failed_iterations.add(iteration)

# Map tcId to result
results = {}
for i, tc in enumerate(tc_ids):
    if i in failed_iterations:
        results[tc] = 'FAIL'
    else:
        results[tc] = 'PASS'

# Update FR-10_ORDER_STATE.md
md_file = 'test-cases/FR-10_ORDER_STATE.md'
with open(md_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

passed_count = sum(1 for res in results.values() if res == 'PASS')
failed_count = sum(1 for res in results.values() if res == 'FAIL')

updated_lines = []
in_table = False
for line in lines:
    if line.strip().startswith('| `FR10-'):
        in_table = True
        parts = line.split('|')
        # The tcId is usually in the first column, like: | `FR10-AI-001` |
        tc = parts[1].strip().replace('`', '')
        if tc in results:
            res = results[tc]
            # Replace NOT RUN or empty Execution column (last column)
            # The structure of the row is: | ID | Type | Req | Priority | Preconditions | Request | Status/body | Post-state | Audit | Execution |
            # We just replace the last column contents before the final '|'
            last_pipe = line.rfind('|')
            second_last_pipe = line.rfind('|', 0, last_pipe - 1)
            old_last_col = line[second_last_pipe+1:last_pipe].strip()
            new_line = line[:second_last_pipe+1] + f" `{res}` " + line[last_pipe:]
            updated_lines.append(new_line)
        else:
            updated_lines.append(line)
    else:
        updated_lines.append(line)

with open(md_file, 'w', encoding='utf-8') as f:
    f.writelines(updated_lines)

print(f"Reconciliation complete. Passed: {passed_count}, Failed: {failed_count}")

# We will also print out the failed test cases and their first error message to help with triage.
if failed_count > 0:
    print("\nFailed Test Cases Details:")
    for fail in data['run'].get('failures', []):
        iteration = fail['cursor']['iteration']
        tc = tc_ids[iteration]
        error_msg = fail.get('error', {}).get('message', '').split('\n')[0]
        print(f" - {tc}: {error_msg}")

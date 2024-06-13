import json

# Load data from test1.json
with open('test1.json') as f:
    data1 = json.load(f)

# Load data from test2.json
data2 = []
with open('test2.json') as f:
    for line in f:
        data2.append(json.loads(line))

# Merge data
for item in data2:
    id = item['id']
    if id in data1:
        item['title'] = data1[id]['title']

# Write merged data to wtq_test3.jsonl
with open('wtq_test3.jsonl', 'w') as f:
    for item in data2:
        f.write(json.dumps(item))
        f.write('\n')

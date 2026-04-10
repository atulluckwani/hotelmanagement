import urllib.request, json
response = urllib.request.urlopen('http://localhost:8000/api/items')
data = json.loads(response.read().decode())
print(f'Total items: {len(data)}')
for item in data:
    print(f"{item['_id']}: {item['name']} (Cuisine {item['cuisine_id']})")

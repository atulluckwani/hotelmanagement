import urllib.request, json, time

print("Testing end-to-end sync...")
print("\n1. Initial items:")
response = urllib.request.urlopen('http://localhost:8000/api/items')
initial_items = json.loads(response.read().decode())
print(f"   Total: {len(initial_items)}")

print("\n2. Adding new item 'Chana Masala'...")
new_item = {
    'name': 'Chana Masala',
    'price': 220,
    'cuisine_id': 1,
    'description': 'Spiced chickpeas curry',
    'dietary_info': 'Veg'
}
req = urllib.request.Request(
    'http://localhost:8000/api/items',
    data=json.dumps(new_item).encode(),
    headers={'Content-Type': 'application/json'}
)
response = urllib.request.urlopen(req)
result = json.loads(response.read().decode())
print(f"   Response: {result['item']['name']} (ID: {result['item']['_id']})")

print("\n3. Verifying item was saved...")
response = urllib.request.urlopen('http://localhost:8000/api/items')
updated_items = json.loads(response.read().decode())
print(f"   Total: {len(updated_items)}")
print(f"   New item exists: {'Chana Masala' in [item['name'] for item in updated_items]}")

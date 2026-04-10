import urllib.request, json

# Test adding a new item
item_data = {
    "name": "Test Samosa",
    "price": 80,
    "cuisine_id": 1,
    "description": "Test samosa item",
    "availability": True,
    "dietary_info": "Veg"
}

req = urllib.request.Request(
    'http://localhost:8000/api/items',
    data=json.dumps(item_data).encode(),
    headers={'Content-Type': 'application/json'}
)

try:
    response = urllib.request.urlopen(req)
    result = json.loads(response.read().decode())
    print("Item created successfully:")
    print(json.dumps(result, indent=2))
except Exception as e:
    print(f"Error: {e}")

# Now fetch all items
print("\n\nFetching all items:")
response = urllib.request.urlopen('http://localhost:8000/api/items')
items = json.loads(response.read().decode())
print(f"Total items: {len(items)}")
for item in items:
    print(f"{item['_id']}: {item['name']} (Cuisine {item['cuisine_id']})")

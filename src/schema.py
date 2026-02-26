import json
import os

schema = {
    "fields": [
        {"name": "transaction_id", "type": "string", "required": True},
        # {"name": "supercell_id", "type": "string", "pattern": "^SC-\d{6}$"},
        # แก้จากเดิมเป็น:
        {"name": "supercell_id", "type": "string", "pattern": r"^SC-\d{6}$"},
        {"name": "item_name", "type": "string"},
        {"name": "amount_local", "type": "number", "min": 0},
        {"name": "currency", "type": "string", "len": 3},
        {"name": "timestamp", "type": "datetime"},
        {"name": "amount_usd", "type": "number"}
    ]
}

schema_dir = os.path.join('data', 'schemas')
os.makedirs(schema_dir, exist_ok=True)

with open(os.path.join(schema_dir, 'financial_schema.json'), 'w') as f:
    json.dump(schema, f, indent=4)

print(f"✅ Schema created at: {os.path.join(schema_dir, 'financial_schema.json')}")
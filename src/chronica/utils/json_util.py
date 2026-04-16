import json

def to_pretty_json(serializable_data):
    return json.dumps(serializable_data, indent=4, ensure_ascii=False)
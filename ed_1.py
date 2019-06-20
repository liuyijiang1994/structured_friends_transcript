import json


def get_json_data(path):
    with open(path, 'r') as f:
        data = json.load(f)
    return data


data = get_json_data('ed/emotion-detection-train.json')

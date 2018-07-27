import json

def dummy_func():
    with open('test/sampleData.json') as f:
        data = json.load(f)
    
    return data
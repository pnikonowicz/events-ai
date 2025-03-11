from fetch.unique import group_similar

def test_unique_group_similar_applies_weights():
    data_json = [
        {"title": "a boy girl tire"},
        {"title": "a banana fruit tire"},
        {"title": "a apple tire"},
        {"title": "a incredible tire"},
    ]
    weights_json = {
        "tire": 10
    }
    
    result = group_similar(data_json, weights_json, .85)

    assert len(result) == 1


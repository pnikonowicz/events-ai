from ai.embeddings_to_recommendation_json import join_recommendation_indexes_with_original_data
from common.data import Data

def test_join_recommendation_indexes_with_original_data():
    recomendation_indexes = [
        {'data_index': 1, 'query_index': None},
        {'data_index': 0, 'query_index': 0}
    ]

    original_query_data_json = ['query_0']
    original_data_json = [
        Data(
            image = 'image_0',
            link = 'link_0',
            title = 'title_0',
            location = 'location_0',
            time = 'time_0',
            similar_events = []
        ), 
        Data(
            image = 'image_1',
            link = 'link_1',
            title = 'title_1',
            location = 'location_1',
            time = 'time_1',
            similar_events = []
        )
    ]

    result = join_recommendation_indexes_with_original_data(recomendation_indexes, original_query_data_json, original_data_json)

    assert len(result) == 2


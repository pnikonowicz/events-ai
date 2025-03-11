from ai.embeddings_to_recommendation_json import grab_similar_items
import numpy as np

def test_grab_similiar_items_ranks_by_similarity_with_something_data_edge_case():
    similarity_matrix = [
        [0.73701256, 0.80360973, 0.78610582, 0.72092243, 0.67967258,
        0.72046494, 0.75843461, 0.75763018, 0.74083195, 0.73275423,
        0.72361401, 0.71278544, 0.71712331, 0.73409511, 0.69361461,
        0.69459076, 0.76458652, 0.74048139, 0.76212396, 0.70116764,
        0.74996434, 0.75297025, 0.74209876, 0.70340372, 0.74471599,
        0.78397588, 0.74711983],
       [0.76809808, 0.84633686, 0.68536792, 0.72690222, 0.6971698 ,
        0.78428538, 0.81450956, 0.77256512, 0.75261413, 0.67172544,
        0.72161782, 0.70335467, 0.72807237, 0.75894172, 0.74482785,
        0.69497116, 0.84478616, 0.7231656 , 0.75210713, 0.69841885,
        0.6656951 , 0.79131938, 0.81294737, 0.74848251, 0.7746592 ,
        0.7289707 , 0.7141847 ]
    ]

    result, _ = grab_similar_items(np.array(similarity_matrix), 10)

    assert 27 == len(result)


def test_grab_similiar_items_ranks_by_similarity_with_data_scattered():
    query_row_1 = [8,10,3]
    query_row_2 = [5,10,7]
    query_row_3 = [8,9,10]
    
    similarity_matrix = [
        query_row_1,
        query_row_2,
        query_row_3
    ]

    result, recomendation_count = grab_similar_items(np.array(similarity_matrix), 10)

    expected_result = [
        {"query_index":  0, "data_index": 1}, 
        {"query_index":  2, "data_index": 2},
        {"query_index": None, "data_index": 0},
    ]

    assert 3 == len(result)
    assert expected_result == result
    assert recomendation_count == 2

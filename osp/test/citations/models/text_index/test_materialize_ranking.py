

import pytest

from osp.citations.models import Citation_Index
from osp.citations.models import Text_Index


pytestmark = pytest.mark.usefixtures('db', 'es')


def test_sort_by_count(add_text, add_citation):

    """
    Results should be sorted by count descending.
    """

    t1 = add_text()
    t2 = add_text()
    t3 = add_text()

    for i in range(3):
        add_citation(t1)

    for i in range(2):
        add_citation(t2)

    for i in range(1):
        add_citation(t3)

    Citation_Index.es_insert()
    Text_Index.es_insert()

    ranks = Citation_Index.rank_texts()
    texts = Text_Index.materialize_ranking(ranks)

    assert texts['hits'][0]['_id'] == str(t1.id)
    assert texts['hits'][1]['_id'] == str(t2.id)
    assert texts['hits'][2]['_id'] == str(t3.id)


@pytest.mark.parametrize('params', [
    lambda x: dict(title=x),
    lambda x: dict(author=[x]),
    lambda x: dict(publisher=x),
    lambda x: dict(journal_title=x),
])
def test_search(params, add_text, add_citation):

    """
    If a free-text search is passed, query against text metadata.
    """

    t1 = add_text(**params('match one'))
    t2 = add_text(**params('two'))
    t3 = add_text(**params('match three'))
    t4 = add_text(**params('four'))

    for i in range(4):
        add_citation(t1)

    for i in range(3):
        add_citation(t2)

    for i in range(2):
        add_citation(t3)

    for i in range(1):
        add_citation(t4)

    Citation_Index.es_insert()
    Text_Index.es_insert()

    ranks = Citation_Index.rank_texts()
    texts = Text_Index.materialize_ranking(ranks, query='match')

    assert len(texts['hits']) == 2
    assert texts['hits'][0]['_id'] == str(t1.id)
    assert texts['hits'][1]['_id'] == str(t3.id)
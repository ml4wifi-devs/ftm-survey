from pybliometrics.scopus import ScopusSearch, AbstractRetrieval


def search(title: str):
    api = ScopusSearch(f'TITLE({title})', subscriber=False)
    return api.results


def citations(eid: str):
    abstract = AbstractRetrieval(eid, view='FULL')
    return [id2eid(r.id) for r in abstract.references]


def id2eid(id: str):
    return f'2-s2.0-{id}'

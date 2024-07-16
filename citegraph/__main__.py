import re
import time
import itertools as it
import bibtexparser
import networkx as nx

from citegraph import scopus

regex = r"""(\\(?:no)?citep?\{(.*?)(?:,\s*(.*?))*\})"""
BIB_SKIP = 182  # @Strings

TITLE = "Indoor Positioning with Wi-Fi Location: A Survey of IEEE 802.11 Fine Timing Measurement Research"


def parse_bibtex(file_path, skip=BIB_SKIP):
    with open(file_path, 'r') as bibtex_file:
        bibtex_file.seek(skip)
        bib_database = bibtexparser.load(bibtex_file)
    return bib_database


def clear_title(title):
    title = title.replace(r'{', '').replace(r'}', '')
    return title


if __name__ == '__main__':
    print('ok')

    with open("paper/template.tex", "rt") as file:
        latex_content = file.read()

    citations = re.findall(regex, latex_content, flags=re.DOTALL)

    keys = set(it.filterfalse(lambda x: x[0] == '\\',
                              it.filterfalse(lambda x: x == "",
                                             it.chain.from_iterable(
                                                 citations))))

    file_path = 'paper/bibliography.bib'
    bib_database = parse_bibtex(file_path)
    refs = [bib_database.entries_dict[k] for k in keys]

    obecne = 0
    edges = []

    for r in refs:
        key = r['ID']

        title = clear_title(r['title'])

        try:
            info = scopus.search(title)
            time.sleep(0.1)
            eid = info[0].eid
            edges.append((TITLE, eid))

            refsrefs = scopus.citations(eid)
            # print(refs)
            for rr in refsrefs:
                edges.append((eid, rr))
            obecne += 1
        except Exception as e:
            print(e, key)

    print(obecne / len(refs))

    G = nx.Graph(edges)

    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(4, 4))

    GG = G.copy()
    nx.write_graphml(G, 'citegraph.graphml')

    from pybliometrics.scopus import ScopusSearch

    q = '''ALL ( "Fine time measurement" ) AND ALL ( "ranging" ) AND ALL ( "FTM" ) OR TITLE-ABS-KEY ( "fine timing measurement" )'''
    ftmpapers = ScopusSearch(q)
    new_papers = []
    Gftm = nx.Graph()
    for p in ftmpapers.results:
        G.add_node(p.eid)
        Gftm.add_node(p.eid)
        new_papers.append(p)
    nx.write_graphml(Gftm, 'ftm.graphml')

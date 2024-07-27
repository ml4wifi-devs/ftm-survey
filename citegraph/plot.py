import matplotlib
import matplotlib.pyplot as plt
import networkx as nx
import seaborn as sns
from matplotlib.cm import viridis

sns.set_style("white")

plt.rcParams["font.family"] = "serif"
import pydot


def int_to_color(num):
    """
  Maps an integer from 0 to 3 to a color value using the plasma palette.

  Args:
    num: An integer between 0 and 3.

  Returns:
    A tuple representing a color in RGB format.
  """

    if not 0 <= num < 3:
        raise ValueError("Input value must be between 0 and 3.")

    # Normalize the input value to a range between 0 and 1
    norm = plt.Normalize(0, 2)

    # Get the color value from the plasma colormap
    color = viridis(norm(num))

    return matplotlib.colors.to_hex(color)


if __name__ == '__main__':
    G = nx.read_graphml('citegraph.graphml')
    Gftm = nx.read_graphml('ftm.graphml')

    for n in Gftm.nodes:
        G.add_node(n)

    new_papers = list(Gftm.nodes)

    mapping = {
        "Indoor Positioning with Wi-Fi Location: A Survey of IEEE 802.11 Fine Timing Measurement Research": "This", }
    nx.relabel_nodes(G, mapping,
                     copy=False)  # Modify the original graph (copy=False)
    Gdot = nx.drawing.nx_pydot.to_pydot(G)

    paths = nx.single_source_dijkstra_path(G, 'This')
    distances = {k: len(v) - 1 for k, v in paths.items()}

    print(max(distances.values()))

    eids = [p for p in new_papers]

    Gdot.set('size', 3.5)
    Gdot.set("overlap", "prism")

    for n in Gdot.get_nodes():
        n.set("shape", "point")

        name = n.get_name()[1:-1]
        n.set("width", 0.1)
        n.set('fixedsize', True)

        if name in eids:
            # n.set("shape", "plain")
            # n.set("label", "X")
            n.set("width", 0.3)

        try:
            n.set("color", int_to_color(distances[name]))
        except KeyError:
            n.set("color", 'gray')
        # print(name)
        if name == "hi":  # This
            n.set("width", 0.5)
            n.set('color', int_to_color(0))

    for e in Gdot.get_edges():
        e.set("color", "#00000020")
        e.set("width", 0.08)

    Gdot.set("layout", "sfdp")

    Gdot.write('citegraph_v2.dot')

    Glegend = pydot.Subgraph(layout="dot", label="Legend",
                             fillcolor="#00000020", style="filled",
                             size="0.5,3.5!", ratio="fill")
    for i in range(3):
        Glegend.add_node(
            pydot.Node(i, color=int_to_color(i), fillcolor=int_to_color(i),
                       shape='circle', width=0.5, fixedwidth=True,
                       style='filled', xlabel=f"{i}", label="", fontsize=20))
    Glegend.add_edge(pydot.Edge(0, 1))
    Glegend.add_edge(pydot.Edge(1, 2))

    Glegend.add_node(
        pydot.Node('Graph distance for paper', shape="underline", fontsize=30))

    Glegend.add_edge(pydot.Edge('Graph distance for paper', 0, style='invis'))

    Glegend.add_node(
        pydot.Node('s0', fillcolor='black', shape='circle', width=0.1,
                   fixedwidth=True, style='filled', label="", xlabel="False",
                   fontsize=20))
    Glegend.add_node(
        pydot.Node('s1', fillcolor='black', shape='circle', width=0.3,
                   fixedwidth=True, style='filled', label="", xlabel="True",
                   fontsize=20))

    Glegend.add_node(
        pydot.Node('sthis', fillcolor='black', shape='circle', width=0.5,
                   fixedwidth=True, style='filled', label="",
                   xlabel="This paper", fontsize=20))
    Glegend.add_edge(pydot.Edge('In FTM query result', 's0', style='invis'))
    #
    Glegend.add_edge(pydot.Edge('s0', 's1', style='invis'))
    Glegend.add_edge(pydot.Edge('s1', 'sthis', style='invis'))
    Glegend.add_node(pydot.Node('legend', style='invis'))

    Glegend.add_node(
        pydot.Node('In FTM query result', shape="underline", fontsize=30))

    Glegend.add_edge(pydot.Edge(2, 'In FTM query result', style='invis'))

    # Glegend.add_edge(pydot.Edge('legend','In FTM query result', style='invis'))
    # Glegend.add_edge(pydot.Edge('legend','Graph distance for paper', style='invis'))

    # Glegend.add_edge(pydot.Edge('s1','sthis', style='invis'))
    # Glegend.add_edge(pydot.Edge('s1','True', style='invis'))
    # Glegend.add_edge(pydot.Edge('s0','False', style='invis'))
    # Glegend.add_edge(pydot.Edge('sthis','This paper', style='invis'))

    # Gdot.add_subgraph(Glegend)
    tmpdot = pydot.Dot(layout="dot", width="0.5in", height="3.5in",
                       fixedwidth=True)
    tmpdot = pydot.Dot(layout="dot", size="0.5,3.5!", ratio="fill")
    tmpdot.add_subgraph(Glegend)
    tmpdot.write_pdf('legend.pdf')
    tmpdot.write_dot('legend.dot')

    Gdot.write_pdf('citegraph_v2.pdf')
    Gdot.write_pdf('citegraph_v2.png')

    # https://matplotlib.org/stable/users/explain/colors/colormaps.html

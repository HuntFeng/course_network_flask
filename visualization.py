from pyvis.network import Network
import pandas as pd
from jinja2 import Template

def make_edge_list(df: pd.DataFrame) -> list:
    from_len = df["prereq"].apply(lambda x: len(x))
    to_list = from_len * df["label"].apply(lambda x: [x])

    edge_list = []
    for n, row in df.iterrows():
        from_len = len(row[2])
        to_list = [row[0]] * from_len
        edges = list(zip(row[2], to_list))
        edge_list += edges
    return edge_list

def make_node_list(df: pd.DataFrame) -> (list, list):
    node_list = list(set(df["label"].to_list() + df["prereq"].sum()))
    title_list = []
    for node in node_list:
        title = df[df["label"]==node]["name"]
        title = node if title.empty else title.item()
        title_list.append(title)
    return node_list, title_list

def make_graph(subjects: list):
    # read data
    df = pd.DataFrame()
    for subject in subjects:
        courses = pd.read_json(f"courses/{subject}.json")
        df = pd.concat([df, courses])

    edge_list = make_edge_list(df)    
    node_list, title_list = make_node_list(df)

    # make graph
    g = Network(
        directed=True, 
        height="650px", 
        width="100%", 
        bgcolor="#222222", 
        font_color="white"
        )
    g.barnes_hut() # spring physics on the edges
    g.inherit_edge_colors(False)

    g.add_nodes(node_list, title=title_list)
    for edge in edge_list:
        g.add_edge(edge[0], edge[1], color="#94c4fc")

    # add neighbor data to node hover data
    for node in g.nodes:
        prereq = df[df["label"]==node["label"]]["prereq"]
        prereq = [] if prereq.empty else prereq.item()
        next_courses = g.neighbors(node["label"]) 
        node["title"] += "<br>Prerequisites:<br>" \
                         + "<br>".join(prereq) \
                         + "<br>Next courses:<br>" \
                         + "<br>".join(next_courses)
        node["value"] = len(next_courses) + len(prereq)
        # highlight the node if it serves as a prerequisites for more than 5 course
        node["font"]["size"] = node["value"]*5
        if node["value"] >= 8:
            node["color"] = "red"
    return g

def make_html_string(g: Network) -> str:
    use_link_template = False
    for n in g.nodes:
        title = n.get("title", None)
        if title:
            if "href" in title:
                """
                this tells the template to override default hover
                mechanic, as the tooltip would move with the mouse
                cursor which made interacting with hover data useless.
                """
                use_link_template = True
                break

    with open(g.path) as html:
        content = html.read()
    template = Template(content)

    nodes, edges, height, width, options = g.get_network_data()
    # check if physics is enabled
    if isinstance(g.options, dict):
        if 'physics' in g.options and 'enabled' in g.options['physics']:
            physics_enabled = g.options['physics']['enabled']
        else:
            physics_enabled = True
    else:
        physics_enabled = g.options.physics.enabled
    html_string = template.render(height=height,
                                width=width,
                                nodes=nodes,
                                edges=edges,
                                options=options,
                                physics_enabled=physics_enabled,
                                use_DOT=g.use_DOT,
                                dot_lang=g.dot_lang,
                                widget=g.widget,
                                bgcolor=g.bgcolor,
                                conf=g.conf,
                                tooltip_link=use_link_template)
    return html_string


if __name__ == "__main__":
    g = make_graph(["math"])
    html_string = make_html_string(g)
    print(html_string[:10], "\n......\n", html_string[-10:])
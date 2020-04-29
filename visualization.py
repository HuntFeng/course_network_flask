from pyvis.network import Network
import pandas as pd

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
    
    g.save_graph("templates/graph.html")

if __name__ == "__main__":
    make_graph(["math"])
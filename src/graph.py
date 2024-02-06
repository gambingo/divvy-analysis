import os

import osmnx as ox
from pandas.core.series import Series

from .directories import DATA_DIR
from src import utils


def download_biking_network(redownload=False):
    """Downloads an osmnx network graph of Chicago."""

    filepath = DATA_DIR / "chicago_bicycle_network_graph.pbz2"

    if not os.path.exists(filepath) or redownload:
        location = "Chicago, Illinois"
        network_type = "bike"
        simplify=True

        graph = ox.graph_from_place(location, 
                                    network_type=network_type, 
                                    simplify=simplify)
    
        utils.save_gherkin(graph, filepath)

    else:
        graph = utils.load_gherkin(filepath)

    return graph
    


def nearest_node(graph, location):
    """
    Find the graph node closest to the specified location. The search is
    unsorted. If multiple nodes are returned, that is because they are all 
    equidistant to the point. This naively returns the first node in that list.
    Often, this happens when the nodes are all right on top of each other, so
    distinguishing is irrelevant.
    ---
    Reminder: Longitude is along the X axis. Latitude is along the Y axis. When 
    we speak we tend to say "lat long", implying latitude comes first. But 
    since latitude goes north/south and longidtude goes east/west, in an X-Y 
    coordinate system, longitude comes first. 

    ---
    Inputs:
        graph:      a networkx graph
        location:   a lat/lng pair as list or tuple (lat expected first)

    Returns:
        graph node id (int)
    """
    lat = location[0]
    lng = location[1]
    node = ox.distance.nearest_nodes(graph, lng, lat)
    
    # `ox.distance.nodes` returns a list when there are multiple
    if not isinstance(node, int):
        node = node[0]

    return node


def nearest_nodes(graph, list_of_lats, list_of_lngs):
    """
    Used when you want to run the above function but in bulk
    """
    if isinstance(list_of_lats, Series):
        list_of_lats = list_of_lats.values.tolist()
    if isinstance(list_of_lngs, Series):
        list_of_lngs = list_of_lngs.values.tolist()

    nodes = ox.distance.nearest_nodes(graph, list_of_lngs, list_of_lats)
    return nodes
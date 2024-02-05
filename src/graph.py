import os

import osmnx as ox

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
    
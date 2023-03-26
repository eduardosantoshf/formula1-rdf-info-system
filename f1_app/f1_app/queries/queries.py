import json
from s4api.graphdb_api import GraphDBApi
from s4api.swagger import ApiClient
from difflib import SequenceMatcher
import re

endpoint = "http://localhost:7200"
repo = "db"

client = ApiClient(endpoint=endpoint)
accessor = GraphDBApi(client)


def get_pilot_info(name):
    query = """
    PREFIX driver: <http://f1/driver/pred/> 

    SELECT ?driver_id ?forename ?surname WHERE
    {
    {
    SELECT DISTINCT ?driver_id ?forename ?surname
    WHERE{
        ?driver_id driver:forename ?forename.
        ?driver_id driver:surname ?surname.
        FILTER regex(?forename, "DRIVER_NAME" , "i")
    }
    }
    UNION
    {
    SELECT DISTINCT ?driver_id ?forename ?surname 
    WHERE{
        ?driver_id driver:forename ?forename.
        ?driver_id driver:surname ?surname.
        FILTER regex(?surname, "DRIVER_NAME" , "i")
    }
    }
    }
    
    """

    query = query.replace("DRIVER_NAME", name)

    payload_query = {"query": query}
    res = accessor.sparql_select(body=payload_query, repo_name=repo)
    print(res)
    res = json.loads(res)

    

get_pilot_info("Lewis")
#
    #all_peoplpe = [(e["p"]["value"], e["name"]["value"]) for e in res['results']['bindings']]
#
    #probably_similar = []
    #for person in all_peoplpe:
    #    sim_ratio = SequenceMatcher(None, person_name.lower(), person[1].lower()).ratio()
    #    if sim_ratio > 0.65:
    #        probably_similar.append((person[0], person[1], sim_ratio))
#
    #return sorted(probably_similar, key=lambda tup: -tup[2])

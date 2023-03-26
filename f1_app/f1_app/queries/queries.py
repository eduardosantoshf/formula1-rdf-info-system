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

    SELECT ?driver_id ?forename ?surname ?nationality WHERE
    {
    {
    SELECT DISTINCT ?driver_id ?forename ?surname ?nationality
    WHERE{
        ?driver_id driver:nationality ?nationality.
        ?driver_id driver:forename ?forename.
        ?driver_id driver:surname ?surname.
        FILTER regex(?forename, "DRIVER_NAME" , "i")
    }
    }
    UNION
    {
    SELECT DISTINCT ?driver_id ?forename ?surname ?nationality
    WHERE{
        ?driver_id driver:nationality ?nationality.
        ?driver_id driver:forename ?forename.
        ?driver_id driver:surname ?surname.
        FILTER regex(?surname, "DRIVER_NAME" , "i")
    }
    }
    }
    
    """

    query = query.replace("DRIVER_NAME", name)

    payload_query = {"query": query}
    response = accessor.sparql_select(body=payload_query, repo_name=repo)

    response = json.loads(response)

    if response['results']['bindings']:
        data = response['results']['bindings'][0]
        print([data['driver_id']['value'].split('/')[-1], data['forename']['value'], data['surname']['value'], data['nationality']['value']])
        return data
    else:
        return []
    

    
        



    

get_pilot_info("Hamilton")
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

import json
from s4api.graphdb_api import GraphDBApi
from s4api.swagger import ApiClient
from difflib import SequenceMatcher
import re

endpoint = "http://localhost:7200"
repo = "db"

client = ApiClient(endpoint=endpoint)
accessor = GraphDBApi(client)


""" Get final standings of all seasons for a specific pilot

    Parameters
    ----------
    code : str
        Pilot code

    Returns
    -------
    list : tuples
        [(driver_code, forename, surname, nationality, season, position, points)]
    """
def pilot_final_standings_by_season(code):
    query = """
    PREFIX driver: <http://f1/driver/pred/> 
    PREFIX driver_final_standings: <http://f1/driver_final_standing/pred/>

    SELECT ?driver_code ?forename ?surname ?nationality ?season ?position ?points WHERE
    {   
        ?driver_id driver:code ?driver_code.
        ?driver_id driver:nationality ?nationality.
        ?driver_id driver:forename ?forename.
        ?driver_id driver:surname ?surname.

        FILTER regex(?driver_code, "DRIVER_CODE" , "i")

        ?driver_id driver:finished_in ?dfs.
        ?dfs driver_final_standings:season ?season.
        ?dfs driver_final_standings:position ?position.
        ?dfs driver_final_standings:points ?points.

    }
    
    """

    query = query.replace("DRIVER_CODE", code)

    payload_query = {"query": query}
    response = accessor.sparql_select(body=payload_query, repo_name=repo)
    #print(response)
    response = json.loads(response)

    if response['results']['bindings']:
        data = response['results']['bindings']
        return [(pilot['driver_code']['value'], 
                 pilot['forename']['value'], 
                 pilot['surname']['value'], 
                 pilot['nationality']['value'],
                 pilot['season']['value'],
                 pilot['position']['value'],
                 pilot['points']['value']) for pilot in data]
    else:
        return []
    
print(pilot_final_standings_by_season("BOT"))
import json
from s4api.graphdb_api import GraphDBApi
from s4api.swagger import ApiClient
from difflib import SequenceMatcher
import re
from pprint import pprint

endpoint = "http://localhost:7200"
repo = "db"

client = ApiClient(endpoint=endpoint)
accessor = GraphDBApi(client)


""" Get drivers with 2+ years of exerience

    Parameters
    ----------

    Returns
    -------
    list : tuples
        [(code, forename, surname, nationality, years)]
    """
def experience_drivers():
    query = """
    PREFIX driver: <http://f1/driver/pred/>
    PREFIX contract: <http://f1/contract/pred/> 

    SELECT (COUNT(DISTINCT ?year) AS ?years) ?code ?forename ?surname ?nationality WHERE
    {
        ?driver_id driver:code ?code.
        ?driver_id driver:forename ?forename.
        ?driver_id driver:surname ?surname.
        ?driver_id driver:nationality ?nationality.

        ?driver_id driver:signed_for ?contract.
        ?contract contract:year ?year.

    }
    GROUP BY ?code ?forename ?surname ?nationality
    HAVING (?years >= 2)
    ORDER BY DESC(?years)
    
    """



    payload_query = {"query": query}
    response = accessor.sparql_select(body=payload_query, repo_name=repo)
    #print(response)
    response = json.loads(response)


    if response['results']['bindings']:
        data = response['results']['bindings']
        return [(pilot['code']['value'], 
                 pilot['forename']['value'], 
                 pilot['surname']['value'], 
                 pilot['nationality']['value'],
                 pilot['years']['value']) for pilot in data]
    else:
        return []
    


""" Top 5 pilots with most championships

    Parameters
    ----------

    Returns
    -------
    list : tuples
        [(driver_code, forename, surname, nationality, number_of_championships)]
    """
def best_pilots():
    query = """
    PREFIX driver: <http://f1/driver/pred/> 
    PREFIX driver_final_standings: <http://f1/driver_final_standing/pred/>

    SELECT ?driver_code ?forename ?surname ?nationality (COUNT(DISTINCT ?season) as ?count) WHERE
    {   
        ?driver_id driver:code ?driver_code.
        ?driver_id driver:nationality ?nationality.
        ?driver_id driver:forename ?forename.
        ?driver_id driver:surname ?surname.

        ?driver_id driver:finished_in ?dfs.
        ?dfs driver_final_standings:season ?season.
        ?dfs driver_final_standings:position ?position.

        FILTER (?position = '1')
    }
    GROUP BY ?driver_code ?forename ?surname ?nationality
    ORDER BY DESC(?count)
    """


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
                 pilot['count']['value']) for pilot in data]
    else:
        return []
    


""" Top 5 teams with most championships

    Parameters
    ----------

    Returns
    -------
    list 
        [team_name, team_nationality, number_of_championships]
    """
def best_teams():
    query = """
    PREFIX team: <http://f1/team/pred/> 
    PREFIX team_final_standings: <http://f1/team_final_standing/pred/>

    SELECT ?team_name ?team_nationality (COUNT(DISTINCT ?season) as ?count) WHERE
    {   
        ?team_id team:name ?team_name.
        ?team_id team:nationality ?team_nationality.

        ?team_id team:finished_in ?tfs.
        ?tfs team_final_standings:season ?season.
        ?tfs team_final_standings:position ?position.

        FILTER (?position = '1')
    }
    GROUP BY ?team_name ?team_nationality
    ORDER BY DESC (?count)

    """

    payload_query = {"query": query}
    response = accessor.sparql_select(body=payload_query, repo_name=repo)

    response = json.loads(response)

    if response['results']['bindings']:
        data = response['results']['bindings']
        return [(pilot['team_name']['value'],
                 pilot['team_nationality']['value'],
                 pilot['count']['value']) for pilot in data]
    else:
        return []    

#pprint(experience_drivers())
#pprint(best_pilots())
pprint(best_teams())
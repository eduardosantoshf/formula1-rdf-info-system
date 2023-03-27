import json
from s4api.graphdb_api import GraphDBApi
from s4api.swagger import ApiClient
from difflib import SequenceMatcher
import re

endpoint = "http://localhost:7200"
repo = "db"

client = ApiClient(endpoint=endpoint)
accessor = GraphDBApi(client)


""" Get information for a specific pilot

    Parameters
    ----------
    name : str
        Pilot name

    Returns
    -------
    list
        [driver_id, forename, surname, nationality]
    """
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
        return [data['driver_id']['value'].split('/')[-1], data['forename']['value'], data['surname']['value'], data['nationality']['value']]
    else:
        return []
    


""" Get all pilots

    Parameters
    ----------
    None

    Returns
    -------
    list : tuples
        [(driver_id, forename, surname, nationality)]
    """
def list_all_pilots():
    query = """
    PREFIX driver: <http://f1/driver/pred/> 

    SELECT ?driver_id ?forename ?surname ?nationality WHERE
    {
        ?driver_id driver:nationality ?nationality.
        ?driver_id driver:forename ?forename.
        ?driver_id driver:surname ?surname.
    }
    
    """

    payload_query = {"query": query}
    response = accessor.sparql_select(body=payload_query, repo_name=repo)

    response = json.loads(response)

    data = response['results']['bindings']

    return([(pilot['driver_id']['value'].split('/')[-1], pilot['forename']['value'], pilot['surname']['value'], pilot['nationality']['value']) for pilot in data])



""" Get all pilots for a specific season

    Parameters
    ----------
    season : int
        year of the season

    Returns
    -------
    list : tuples
        [(driver_id, forename, surname, nationality)]
    """
def get_pilots_by_season(season):

    season = str(season)

    query = """
    PREFIX driver: <http://f1/driver/pred/> 
    PREFIX season: <http://f1/season/pred/>

    SELECT ?driver_id ?forename ?surname ?nationality ?year WHERE
    {
        ?driver_id driver:drived_on ?s.
        ?driver_id driver:forename ?forename.
        ?driver_id driver:surname ?surname.
        ?driver_id driver:nationality ?nationality.
        ?s  season:year ?year.
        FILTER regex(?year, "SEASON_YEAR" , "i")
    }
    
    """
    query = query.replace("SEASON_YEAR", season)
    payload_query = {"query": query}
    response = accessor.sparql_select(body=payload_query, repo_name=repo)

    response = json.loads(response)

    data = response['results']['bindings']

    return([(pilot['driver_id']['value'].split('/')[-1], pilot['forename']['value'], pilot['surname']['value'], pilot['nationality']['value']) for pilot in data])
    

# TODO not working yet
#def get_pilots_by_season_and_team(season, team):
#
#    season = str(season)
#
#    query_2 = """
#    PREFIX team: <http://f1/team/pred/>
#    PREFIX season: <http://f1/season/pred/>
#
#    SELECT ?name ?year WHERE
#    {
#        ?t team:name ?name.
#        ?t team:participated_in ?s.
#        ?s season:year ?year.
#        FILTER regex(?year, "SEASON_YEAR", "i")
#    }
#    
#    """
#
#    query_2 = query_2.replace("SEASON_YEAR", season)
#    query_2 = query_2.replace("TEAM_NAME", team)
#    #print(query)
#    payload_query = {"query": query_2}
#    response = accessor.sparql_select(body=payload_query, repo_name=repo)
#    print(response)
#    response = json.loads(response)
#    
#
#    data = response['results']['bindings']
#
#    return([(pilot['driver_id']['value'].split('/')[-1], pilot['forename']['value'], pilot['surname']['value'], pilot['nationality']['value']) for pilot in data])
    
        



    

#print(get_pilot_info("Hamilton"))
#print("\n")
#print(list_all_pilots())
#print("\n")
#print(get_pilots_by_season(2022))
#print(get_pilots_by_season_and_team(2020, "Mercedes"))

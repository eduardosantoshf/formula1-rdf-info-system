# -*- coding: utf-8 -*-
# @Author: Eduardo Santos
# @Date:   2023-04-08 17:46:26
# @Last Modified by:   Eduardo Santos
# @Last Modified time: 2023-04-09 20:49:26

import json
from s4api.graphdb_api import GraphDBApi
from s4api.swagger import ApiClient
from pprint import pprint
import requests

from drivers_queries import get_pilot_info
from teams_queries import *

endpoint = "http://localhost:7200"
repo = "db"

headers = {
    "Content-Type": "application/sparql-update",
    "Accept": "application/json"
}

client = ApiClient(endpoint=endpoint)
accessor = GraphDBApi(client)

""" Delete driver

    Parameters
    ----------
    name : str
        Driver's name
    """
def delete_pilot(driver):
    query = """
    PREFIX driver: <http://f1/driver/pred/> 
    
    DELETE {
        ?s ?p ?o .
    }
    WHERE {
        ?s driver:forename DRIVER_NAME ;
        driver:surname ?surname ;
        driver:nationality ?nationality ;
        driver:code ?code ;
        ?p ?o .
    }
    """

    query = query.replace("DRIVER_NAME", driver)

    response = requests.post(
        f"{endpoint}/repositories/{repo}/statements",
        headers = headers,
        data = query
    )


""" Delete team

    Parameters
    ----------
    name : str
        Teams's name
    """
def delete_team(team):
    query = """
    PREFIX team: <http://f1/team/pred/> 
    
    DELETE {
        ?s ?p ?o .
    }
    WHERE {
        ?s team:name TEAM_NAME ;
        team:nationality ?nationality ;
        ?p ?o .
    }
    """

    query = query.replace("TEAM_NAME", team)

    response = requests.post(
        f"{endpoint}/repositories/{repo}/statements",
        headers = headers,
        data = query
    )


""" Delete contract

    Parameters
    ----------
    driver : str
        Driver's name
    team : str
        Teams's name
    season : int
        Contract's year
    """
def delete_contract(driver, team, season):
    driver_id = get_pilot_info(driver)[0]
    team_id = get_team_info(team)[team][0][0][0]
    
    query = """
    PREFIX contract: <http://f1/contract/pred/>

    DELETE {
    ?contract ?p ?o .
    }
    WHERE {
        ?contract contract:team TEAM_NAME ;
                contract:driver DRIVER_NAME ;
                contract:year CONTRACT_YEAR ;
                ?p ?o .
    }
    """

    query = query.replace("TEAM_NAME", str(team_id))
    query = query.replace("DRIVER_NAME", str(driver_id))
    query = query.replace("CONTRACT_YEAR", str(season))

    response = requests.post(
        f"{endpoint}/repositories/{repo}/statements",
        headers = headers,
        data = query
    )


""" Create driver

    Parameters
    ----------
    forename : str
        Driver's forename
    surname : str
        Driver's surname
    nationality : str
        Driver's nationality
    code : str
        Driver's code
    """
def create_pilot(forename, surname, nationality, code):

    #TODO: generate id to driver
    
    query = f"""
    PREFIX driver: <http://f1/driver/pred/>

    INSERT DATA {{
        _:driver driver:forename "{forename}" ;
                 driver:surname "{surname}" ;
                 driver:nationality "{nationality}" ;
                 driver:code "{code}" .
    }}
    """


    response = requests.post(
        f"{endpoint}/repositories/{repo}/statements",
        headers = headers,
        data = query
    )


#create_pilot("Santos", "Edu", "Portuguese", "SAN")


""" Create team

    Parameters
    ----------
    name : str
        Team's name
    nationality : str
        Team's nationality
    """
def create_team(name, nationality):
    
    #TODO: generate id to team

    query = f"""
    PREFIX team: <http://f1/team/pred/>

    INSERT DATA {{
        _:team team:name "{name}" ;
                 team:nationality "{nationality}" 
    }}
    """


    response = requests.post(
        f"{endpoint}/repositories/{repo}/statements",
        headers = headers,
        data = query
    )
    print(response)

#create_team("EI", "Portuguese")


""" Create contract

    Parameters
    ----------
    driver : str
        Driver's name
    team : str
        Team's name
    season : int
        Season
    """
def create_contract(driver, team, season):
    
    #TODO: generate id to team

    query = f"""
    PREFIX contract: <http://f1/contract/pred/>

    INSERT DATA {{
        _:contract contract:driver "{driver}" ;
                 contract:team "{team}" ;
                 contract:year "{season}" 
    }}
    """


    response = requests.post(
        f"{endpoint}/repositories/{repo}/statements",
        headers = headers,
        data = query
    )
    print(response)

a = get_pilot_info("Santos")
print(a)
create_contract("1", "214", 2023)
#create_contract("genid-e61b5268ba1f4122b3f9d8359203b0c917483-driver", "_:genid-e61b5268ba1f4122b3f9d8359203b0c920189-team", 2023)
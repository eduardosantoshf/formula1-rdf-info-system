# -*- coding: utf-8 -*-
# @Author: Eduardo Santos
# @Date:   2023-04-08 17:46:26
# @Last Modified by:   Eduardo Santos
# @Last Modified time: 2023-04-09 20:48:25

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



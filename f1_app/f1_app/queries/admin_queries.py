# -*- coding: utf-8 -*-
# @Author: Eduardo Santos
# @Date:   2023-04-08 17:46:26
# @Last Modified by:   Eduardo Santos
# @Last Modified time: 2023-04-08 21:00:49

import json
from s4api.graphdb_api import GraphDBApi
from s4api.swagger import ApiClient
from difflib import SequenceMatcher
import re
from pprint import pprint
import requests

from drivers_queries import get_pilot_info

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

def delete_pilot(name):
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

    query = query.replace("DRIVER_NAME", name)

    response = requests.post(
        f"{endpoint}/repositories/{repo}/statements",
        headers = headers,
        data = query
    )
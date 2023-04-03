# -*- coding: utf-8 -*-
# @Author: Eduardo Santos
# @Date:   2023-03-26 22:49:05
# @Last Modified by:   Eduardo Santos
# @Last Modified time: 2023-03-26 23:55:44

import json
from s4api.graphdb_api import GraphDBApi
from s4api.swagger import ApiClient
from difflib import SequenceMatcher
import re

endpoint = "http://localhost:7200"
repo = "db"

client = ApiClient(endpoint=endpoint)
accessor = GraphDBApi(client)


def get_team_info(team_name):
    query = """
    PREFIX team: <http://f1/team/pred/> 

    SELECT DISTINCT ?team_id ?team_name ?team_nationality
    WHERE{ 
        ?team_id team:nationality ?team_nationality.
        ?team_id team:name ?team_name.
    }
    
    
    """

    payload_query = {"query": query}
    res = accessor.sparql_select(body=payload_query, repo_name=repo)
    res = json.loads(res)

    all_teams = [(t["team_name"]["value"], t["team_nationality"]["value"]) for t in res['results']['bindings']]

    probably_similar = {}
    for team in all_teams:
        sim_ratio = SequenceMatcher(None, team_name.lower(), team[0].lower()).ratio()
        if sim_ratio > 0.50:
            if team_name not in probably_similar:
                probably_similar[team_name] = [((team[0], team[1]), sim_ratio)]
            else:
                probably_similar[team_name].append(((team[0], team[1]), sim_ratio))

    most_similar = {k: sorted(v, key = lambda x: x[1], reverse = True)[:3] for k, v in probably_similar.items()}

    #print(f"Most similar: {most_similar}")
    return most_similar

def get_all_teams():
    query = """
    PREFIX team: <http://f1/team/pred/> 

    SELECT DISTINCT ?team_id ?team_name ?team_nationality
    WHERE{ 
        ?team_id team:nationality ?team_nationality.
        ?team_id team:name ?team_name.
    }
    """

    #query = query.replace("DRIVER_NAME", name)

    payload_query = {"query": query}
    res = accessor.sparql_select(body=payload_query, repo_name=repo)
    res = json.loads(res)

    all_teams = [(t["team_name"]["value"], t['team_nationality']['value']) for t in res['results']['bindings']]

    print(all_teams)

    return all_teams

get_all_teams()


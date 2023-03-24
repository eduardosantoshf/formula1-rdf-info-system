import json
from s4api.graphdb_api import GraphDBApi
from s4api.swagger import ApiClient
from difflib import SequenceMatcher
import re

endpoint = "http://localhost:7200"
repo = "database_ws"

client = ApiClient(endpoint=endpoint)
accessor = GraphDBApi(client)

query = """ 
    SELECT DISTINCT ?subj ?pred ?obj
    WHERE {
        <http://movies.org/en/bad_taste> ?pred ?obj
    }
    LIMIT 10

"""

res = accessor.sparql_select(body={"query": query}, repo_name=repo)

print(res)

update = """
    INSERT DATA { <http://movies.org/en/bad_taste> <http://movies.org/pred/starring> <http://movies.org/guid/9202a8c04000641f80000000010cf900> . }
"""

res2 = accessor.sparql_update(body={"update": update}, repo_name=repo)

print(res2)



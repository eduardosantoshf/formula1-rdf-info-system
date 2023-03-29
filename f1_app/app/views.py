from django.shortcuts import render
from f1_app.queries import races_queries
from f1_app.queries import standings_queries

# Create your views here.

def results(request, season):
    results = standings_queries.pilots_season_final_standings(season)
    if len(results):
        data = {'data': results}
        print(data)
    else:
        data = {'error': True}
        print("error")
    return render(request, "results.html", data)

def teams(request):
    return render(request, "teams.html")
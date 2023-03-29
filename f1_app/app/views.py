from django.shortcuts import render
from f1_app.queries import races_queries
from f1_app.queries import standings_queries

# Create your views here.

cities = {
    "Australian Grand Prix"
    "Bahrain Grand Prix"
    "Chinese Grand Prix"
    "Azerbaijan Grand Prix"
    "Spanish Grand Prix"
    "Monaco Grand Prix"
    "Canadian Grand Prix"
    "French Grand Prix"
    "Austrian Grand Prix"
    "British Grand Prix"
    "German Grand Prix"
    "Hungarian Grand Prix"
    "Belgian Grand Prix"
    "Italian Grand Prix"
    "Singapore Grand Prix"
    "Russian Grand Prix"
    "Japanese Grand Prix"
    "Mexican Grand Prix"
    "United States Grand Prix"
    "Brazilian Grand Prix"
    "Abu Dhabi Grand Prix"
    "Styrian Grand Prix"
    "70th Anniversary Grand Prix"
    "Tuscan Grand Prix"
    "Eifel Grand Prix"
    "Portuguese Grand Prix"
    "Emilia Romagna Grand Prix"
    "Turkish Grand Prix"
    "Sakhir Grand Prix"
    "Dutch Grand Prix"
    "Mexico City Grand Prix"
    "São Paulo Grand Prix"
    "Qatar Grand Prix"
    "Saudi Arabian Grand Prix"
    "Miami Grand Prix"
}

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

def races(request, season):
    races = races_queries.races_by_season(season)
    print(races)
    if len(races):
        data = {'data': races}
    else:
        data = {'error': True}
        print("error")
    return render(request, "races.html", data)
from django.shortcuts import render
from f1_app.queries import races_queries
from f1_app.queries import standings_queries
from f1_app.queries import teams_queries

# Create your views here.

cities = {
    "Australian Grand Prix" : "Melbourne, Australia",
    "Bahrain Grand Prix" : "Sakhir, Bahrain",
    "Chinese Grand Prix" : "Shanghai, China",
    "Azerbaijan Grand Prix" : "Baku, Azerbaijan",
    "Spanish Grand Prix" : "Montmeló, Spain",
    "Monaco Grand Prix" : "Monaco, France",
    "Canadian Grand Prix" : "Montreal, Canada",
    "French Grand Prix" : "Le Castellet, France",
    "Austrian Grand Prix" : "Spielberg, Austria",
    "British Grand Prix" : "Silverstone, UK",
    "German Grand Prix" : "Nürburg, Germany",
    "Hungarian Grand Prix" : "Budapest, Hungaria",
    "Belgian Grand Prix" : "Ardennes, Belgium",
    "Italian Grand Prix" : "Milan, Italy",
    "Singapore Grand Prix" : "Marina Bay, Singapore",
    "Russian Grand Prix" : "Sochi Autodrom, Russia",
    "Japanese Grand Prix" : "Shizuoka, Japan",
    "Mexican Grand Prix" : "Mexico City, Mexico",
    "United States Grand Prix" : "Austin, Texas, USA",
    "Brazilian Grand Prix" : "São Paulo, Brazil",
    "Abu Dhabi Grand Prix" : "Yas Island, UAE",
    "Styrian Grand Prix" : "Styria, Austria",
    "70th Anniversary Grand Prix" : "Silverstone, UK",
    "Tuscan Grand Prix" : "Tuscany, Italy",
    "Eifel Grand Prix" : "Nürburg, Germany",
    "Portuguese Grand Prix" : "Portimão, Portugal",
    "Emilia Romagna Grand Prix" : "Emilia Romagna, Italy",
    "Turkish Grand Prix" : "Istambul, Turkey",
    "Sakhir Grand Prix" : "Sakhir, Bahrain",
    "Dutch Grand Prix" : "Amsterdam, Netherlands",
    "Mexico City Grand Prix" : "Mexico City, Mexico",
    "São Paulo Grand Prix" : "São Paulo, Brazil",
    "Qatar Grand Prix" : "Doha, Qatar",
    "Saudi Arabian Grand Prix" : "Jeddah, Saudi Arabia",
    "Miami Grand Prix" : "Florida, USA"
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
    teams = teams_queries.get_all_teams()
    data = {'data': teams}
    print(data)
    return render(request, "teams.html", data)

def races(request, season):
    races = races_queries.races_by_season(season)
    new_races = []
    for race in races:
        new_races.append((race[0], race[1], cities[race[1]], race[3]))

    print(new_races)
    if len(new_races):
        data = {'data': new_races}
    else:
        data = {'error': True}
        print("error")
    return render(request, "races.html", data)
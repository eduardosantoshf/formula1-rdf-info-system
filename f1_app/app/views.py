from django.shortcuts import render
from f1_app.queries import races_queries
from f1_app.queries import standings_queries
from f1_app.queries import teams_queries
from f1_app.queries import drivers_queries

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
    final_teams = []
    for team in teams:
        championships = standings_queries.team_total_championships(team[0])
        if championships:
            final_teams.append((team[0], team[1], championships[2]))
        else:
            final_teams.append((team[0], team[1], '0'))
    
    sorted_list = sorted(final_teams, key=lambda x: x[2], reverse=True)

    data = {'data': sorted_list}
    print(data)
    return render(request, "teams.html", data)

def drivers(request):
    drivers = drivers_queries.list_all_pilots()
    final_drivers = []
    for driver in drivers:
        championships = standings_queries.pilot_total_championships(driver[0])
        if championships:
            final_drivers.append((driver[0], driver[1],  driver[2],  driver[3], championships[4]))
        else:
            final_drivers.append((driver[0], driver[1],  driver[2],  driver[3], '0'))
    
    sorted_list = sorted(final_drivers, key=lambda x: x[4], reverse=True)

    data = {'data': sorted_list}
    print(data)
    return render(request, "drivers.html", data)

def races(request, season):
    races = races_queries.races_by_season(season)
    new_races = []
    for race in races:
        new_races.append((race[0], race[1], cities[race[1]], race[3], season))

    print(new_races)
    if len(new_races):
        data = {'data': new_races}
    else:
        data = {'error': True}
        print("error")
    return render(request, "races.html", data)

def race_info(request, season, race_name):
    race_info = races_queries.all_pilots_standings_by_race_by_season(race_name, season)
    print(race_info)
    if len(race_info):
        data = {'data': race_info}
    else:
        data = {'error': True}
    return render(request, "race-modal.html", data)
    
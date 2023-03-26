# -*- coding: utf-8 -*-
# @Author: Eduardo Santos
# @Date:   2023-03-25 19:38:14
# @Last Modified by:   Eduardo Santos
# @Last Modified time: 2023-03-26 18:53:21

import csv

base_rdf = "http://f1"

season_triples = set()
driver_triples = set()
team_triples = set()
race_triples = set()
driver_standing_triples = set()
driver_final_standing_triples = set()
team_final_standing_triples = set()

triples = [
    season_triples,
    driver_triples,
    team_triples,
    race_triples,
    driver_standing_triples,
    driver_final_standing_triples,
    team_final_standing_triples
]

### Load drivers
drivers_dict = {}
with open('../datasets/drivers.csv', 'r') as file:
    file.readline()
    reader = csv.reader(file)

    for row in reader:
        driver_id = row[0]
        row.pop(0)
        drivers_dict[driver_id] = row

### Load races and create Season entities
races_dict = {}
with open('../datasets/races.csv', 'r') as file:
    file.readline()
    reader = csv.reader(file)

    processed_seasons = []

    for row in reader:
        race_id = row[0]
        row.pop(0)

        season = row[0]
        season_base_rdf = "<{}/season".format(base_rdf)
        
        if season not in processed_seasons:
            season_id = "{}/id/{}>".format(season_base_rdf, race_id)
            season_year_pred = "{}/pred/year>".format(season_base_rdf)
            season_year = "\"{}\"".format(season)
            season_triples.add("{} {} {} .".format(season_id, season_year_pred, season_year))
            processed_seasons.append(season)


        row.append(season_id)
        races_dict[race_id] = row

### Load status
status_dict = {}
with open('../datasets/status.csv', 'r') as file:
    file.readline()
    reader = csv.reader(file)

    for row in reader:
        status_dict[row[0]] = row[1]


teams_dict = {}
with open("../datasets/teams.csv") as file:
    file.readline()
    reader = csv.reader(file)

    for row in reader:
        t_id = row[0]
        row.pop(0)
        teams_dict[t_id] = row

        team_base_rdf = "<{}/team".format(base_rdf)

        # Teams
        team_id = "{}/id/{}>".format(team_base_rdf, t_id)

        team_info = teams_dict[t_id]

        team_code_pred = "{}/pred/name>".format(team_base_rdf)
        team_name = "\"{}\"".format(team_info[1])
        team_triples.add("{} {} {} .".format(team_id, team_code_pred, team_name))

        team_code_pred = "{}/pred/nationality>".format(team_base_rdf)
        team_nationality = "\"{}\"".format(team_info[2])
        team_triples.add("{} {} {} .".format(team_id, team_code_pred, team_nationality))


with open("../datasets/team_final_standings.csv") as file:
    file.readline()
    reader = csv.reader(file)

    for row in reader:
        team_final_standing_base_rdf = "<{}/team_final_standing".format(base_rdf)

        team_final_standing_id = "{}/id/{}>".format(team_final_standing_base_rdf, row[0])

        team_final_standing_season_pred = "{}/pred/season>".format(team_final_standing_base_rdf)
        team_final_standing_season = "\"{}\"".format(races_dict[row[1]][0])
        team_final_standing_triples.add("{} {} {} .".format(team_final_standing_id, team_final_standing_season_pred, team_final_standing_season))

        team_final_standing_position_pred = "{}/pred/position>".format(team_final_standing_base_rdf)
        team_final_standing_position = "\"{}\"".format(row[4])
        team_final_standing_triples.add("{} {} {} .".format(team_final_standing_id, team_final_standing_position_pred, team_final_standing_position))

        team_final_standing_points_pred = "{}/pred/points>".format(team_final_standing_base_rdf)
        team_final_standing_points = "\"{}\"".format(row[3])
        team_final_standing_triples.add("{} {} {} .".format(team_final_standing_id, team_final_standing_points_pred, team_final_standing_points))

        team_id = "{}/id/{}>".format(team_base_rdf, row[2])
        team_final_standing_pred = "{}/pred/finished_in>".format(team_base_rdf)
        team_triples.add("{} {} {} .".format(team_id, team_final_standing_pred, team_final_standing_id))


with open('../datasets/results.csv', 'r') as file:
    file.readline()
    reader = csv.reader(file)

    processed_races = []
    processed_drivers = []

    for row in reader:
        # Races
        race_base_rdf = "<{}/race".format(base_rdf)
        r_id = row[1]
        race_id = "{}/id/{}>".format(race_base_rdf, r_id)
        if r_id not in processed_races:
            race_info = races_dict[r_id]

            race_season_pred = "{}/pred/season>".format(race_base_rdf)
            race_season = "\"{}\"".format(race_info[0])
            race_triples.add("{} {} {} .".format(race_id, race_season_pred, race_season))

            race_round_pred = "{}/pred/round>".format(race_base_rdf)
            race_round = "\"{}\"".format(race_info[1])
            race_triples.add("{} {} {} .".format(race_id, race_round_pred, race_round))

            race_name_pred = "{}/pred/name>".format(race_base_rdf)
            race_name = "\"{}\"".format(race_info[2])
            race_triples.add("{} {} {} .".format(race_id, race_name_pred, race_name))

            processed_races.append(r_id)

        # Drivers
        driver_base_rdf = "<{}/driver".format(base_rdf)
        d_id = row[2]
        driver_id = "{}/id/{}>".format(driver_base_rdf, d_id)
        if d_id not in processed_drivers:
            driver_info = drivers_dict[d_id]

            driver_code_pred = "{}/pred/code>".format(driver_base_rdf)
            driver_code = "\"{}\"".format(driver_info[0])
            driver_triples.add("{} {} {} .".format(driver_id, driver_code_pred, driver_code))

            driver_surname_pred = "{}/pred/surname>".format(driver_base_rdf)
            driver_surname = "\"{}\"".format(driver_info[1])
            driver_triples.add("{} {} {} .".format(driver_id, driver_surname_pred, driver_surname))

            driver_forename_pred = "{}/pred/forename>".format(driver_base_rdf)
            driver_forename = "\"{}\"".format(driver_info[2])
            driver_triples.add("{} {} {} .".format(driver_id, driver_forename_pred, driver_forename))

            driver_nationality_pred = "{}/pred/nationality>".format(driver_base_rdf)
            driver_nationality = "\"{}\"".format(driver_info[3])
            driver_triples.add("{} {} {} .".format(driver_id, driver_nationality_pred, driver_nationality))

            processed_races.append(r_id)

        # Driver Standing
        driver_standing_base_rdf = "<{}/driver_standing".format(base_rdf)
        driver_standing_id = "{}/id/{}>".format(driver_standing_base_rdf, row[0])

        driver_standing_grid_pred = "{}/pred/grid>".format(driver_standing_base_rdf)
        driver_standing_grid = "\"{}\"".format(row[4])
        driver_standing_triples.add("{} {} {} .".format(driver_standing_id, driver_standing_grid_pred, driver_standing_grid))

        driver_standing_position_pred = "{}/pred/position>".format(driver_standing_base_rdf)
        driver_standing_position = "\"{}\"".format(row[5])
        driver_standing_triples.add("{} {} {} .".format(driver_standing_id, driver_standing_position_pred, driver_standing_position))

        driver_standing_points_pred = "{}/pred/points>".format(driver_standing_base_rdf)
        driver_standing_points = "\"{}\"".format(row[6])
        driver_standing_triples.add("{} {} {} .".format(driver_standing_id, driver_standing_points_pred, driver_standing_points))

        driver_standing_status_pred = "{}/pred/status>".format(driver_standing_base_rdf)
        driver_standing_status = "\"{}\"".format(status_dict[row[7]])
        driver_standing_triples.add("{} {} {} .".format(driver_standing_id, driver_standing_status_pred, driver_standing_status))

        driver_standing_driver_pred = "{}/pred/for>".format(driver_standing_base_rdf)
        driver_standing_triples.add("{} {} {} .".format(driver_standing_id, driver_standing_driver_pred, driver_id))

        driver_standing_race_pred = "{}/pred/at>".format(driver_standing_base_rdf)
        driver_standing_triples.add("{} {} {} .".format(driver_standing_id, driver_standing_race_pred, race_id))

        driver_code_pred = "{}/pred/has>".format(driver_base_rdf)
        driver_triples.add("{} {} {} .".format(driver_id, driver_code_pred, driver_standing_id))

        race_round_pred = "{}/pred/has>".format(race_base_rdf)
        race_triples.add("{} {} {} .".format(race_id, race_round_pred, driver_standing_id))

        season_id = races_dict[r_id][3]
        # Driver - Season
        driver_season_pred = "{}/pred/drived_on>".format(driver_base_rdf)
        driver_triples.add("{} {} {} .".format(driver_id, driver_season_pred, season_id))

        # Season - Driver
        season_driver_pred = "{}/pred/had_driver>".format(season_base_rdf)
        season_triples.add("{} {} {} .".format(season_id, season_driver_pred, driver_id))

        # Team - Season
        team_id = "{}/id/{}>".format(team_base_rdf, row[3])
        team_season_pred = "{}/pred/participated_in>".format(team_base_rdf)
        team_triples.add("{} {} {} .".format(team_id, team_season_pred, season_id))

        # Season - Team
        season_team_pred = "{}/pred/had_team>".format(season_base_rdf)
        season_triples.add("{} {} {} .".format(season_id, season_team_pred, team_id))


with open('../datasets/driver_final_standings.csv', 'r') as file:
    file.readline()
    reader = csv.reader(file)

    for row in reader:
        driver_final_standing_base_rdf = "<{}/driver_final_standing".format(base_rdf)

        driver_final_standing_id = "{}/id/{}>".format(driver_final_standing_base_rdf, row[0])

        driver_final_standing_season_pred = "{}/pred/season>".format(driver_final_standing_base_rdf)
        driver_final_standing_season = "\"{}\"".format(races_dict[row[1]][0])
        driver_final_standing_triples.add("{} {} {} .".format(driver_final_standing_id, driver_final_standing_season_pred, driver_final_standing_season))

        driver_final_standing_points_pred = "{}/pred/points>".format(driver_final_standing_base_rdf)
        driver_final_standing_points = "\"{}\"".format(row[3])
        driver_final_standing_triples.add("{} {} {} .".format(driver_final_standing_id, driver_final_standing_points_pred, driver_final_standing_points))

        driver_final_standing_position_pred = "{}/pred/position>".format(driver_final_standing_base_rdf)
        driver_final_standing_position = "\"{}\"".format(row[4])
        driver_final_standing_triples.add("{} {} {} .".format(driver_final_standing_id, driver_final_standing_position_pred, driver_final_standing_position))

        driver_id = "{}/id/{}>".format(driver_base_rdf, row[2])
        driver_final_standing_pred = "{}/pred/finished_in>".format(driver_base_rdf)
        driver_triples.add("{} {} {} .".format(driver_id, driver_final_standing_pred, driver_final_standing_id))

    #for i in driver_standing_triples:
    #    print(i)

    #for i in team_triples:
    #    print(i)

f1_set = set()
for triple in triples:
    for t in triple: 
        f1_set.add(t)
# save triples on .nt file
with open("../datasets/f1.nt", "w") as output_file:
    for s in f1_set:
        output_file.write("{}\n".format(s))
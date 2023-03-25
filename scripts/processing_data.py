import re
import csv
import random

### Load drivers
drivers_dict = {}
with open('../datasets/drivers.csv', 'r') as file:
    file.readline()
    reader = csv.reader(file)

    for row in reader:
        driver_id = row[0]
        row.pop(0)
        drivers_dict[driver_id] = row

### Load races
races_dict = {}
with open('../datasets/races.csv', 'r') as file:
    file.readline()
    reader = csv.reader(file)

    for row in reader:
        race_id = row[0]
        row.pop(0)
        races_dict[race_id] = row

### Load status
status_dict = {}
with open('../datasets/status.csv', 'r') as file:
    file.readline()
    reader = csv.reader(file)

    for row in reader:
        status_dict[row[0]] = row[1]

base_rdf_list = ["http://f1"]
base_driver_rdf_list =["http://f1/driver"]

driver_triples = set()
race_triples = set()
driver_standing_triples = set()
driver_final_standing_triples = set()

driver_id = ""
with open('../datasets/results.csv', 'r') as file:
    file.readline()
    reader = csv.reader(file)

    processed_races = []
    processed_drivers = []

    for row in reader:
        chosen_base_rdf = random.choice(base_rdf_list)

        # Races
        r_id = row[1]
        race_id = "<{}/race_id/{}>".format(chosen_base_rdf, r_id)
        if r_id not in processed_races:
            race_info = races_dict[r_id]

            race_season_pred = "<{}/pred/season>".format(chosen_base_rdf)
            race_season = "\"{}\"".format(race_info[0])
            race_triples.add("{} {} {} .".format(race_id, race_season_pred, race_season))

            race_round_pred = "<{}/pred/round>".format(chosen_base_rdf)
            race_round = "\"{}\"".format(race_info[1])
            race_triples.add("{} {} {} .".format(race_id, race_round_pred, race_round))

            race_name_pred = "<{}/pred/name>".format(chosen_base_rdf)
            race_name = "\"{}\"".format(race_info[2])
            race_triples.add("{} {} {} .".format(race_id, race_name_pred, race_name))

            processed_races.append(r_id)

        # Drives
        d_id = row[2]
        driver_id = "<{}/driver_id/{}>".format(chosen_base_rdf, d_id)
        if d_id not in processed_drivers:
            driver_info = drivers_dict[d_id]

            driver_code_pred = "<{}/pred/code>".format(chosen_base_rdf)
            driver_code = "\"{}\"".format(driver_info[0])
            driver_triples.add("{} {} {} .".format(driver_id, driver_code_pred, driver_code))

            driver_surname_pred = "<{}/pred/surname>".format(chosen_base_rdf)
            driver_surname = "\"{}\"".format(driver_info[1])
            driver_triples.add("{} {} {} .".format(driver_id, driver_surname_pred, driver_surname))

            driver_forename_pred = "<{}/pred/forename>".format(chosen_base_rdf)
            driver_forename = "\"{}\"".format(driver_info[2])
            driver_triples.add("{} {} {} .".format(driver_id, driver_forename_pred, driver_forename))

            driver_nationality_pred = "<{}/pred/nationality>".format(chosen_base_rdf)
            driver_nationality = "\"{}\"".format(driver_info[3])
            driver_triples.add("{} {} {} .".format(driver_id, driver_nationality_pred, driver_nationality))

            processed_races.append(r_id)

        # Driver Standing
        driver_standing_id = "<{}/driver_standing_id/{}>".format(chosen_base_rdf, row[0])

        driver_standing_grid_pred = "<{}/pred/grid>".format(chosen_base_rdf)
        driver_standing_grid = "\"{}\"".format(row[4])
        driver_standing_triples.add("{} {} {} .".format(driver_standing_id, driver_standing_grid_pred, driver_standing_grid))

        driver_standing_position_pred = "<{}/pred/position>".format(chosen_base_rdf)
        driver_standing_position = "\"{}\"".format(row[5])
        driver_standing_triples.add("{} {} {} .".format(driver_standing_id, driver_standing_position_pred, driver_standing_position))

        driver_standing_points_pred = "<{}/pred/points>".format(chosen_base_rdf)
        driver_standing_points = "\"{}\"".format(row[6])
        driver_standing_triples.add("{} {} {} .".format(driver_standing_id, driver_standing_points_pred, driver_standing_points))

        driver_standing_status_pred = "<{}/pred/status>".format(chosen_base_rdf)
        driver_standing_status = "\"{}\"".format(status_dict[row[7]])
        driver_standing_triples.add("{} {} {} .".format(driver_standing_id, driver_standing_status_pred, driver_standing_status))

        driver_standing_driver_pred = "<{}/pred/for>".format(chosen_base_rdf)
        driver_standing_triples.add("{} {} {} .".format(driver_standing_id, driver_standing_driver_pred, driver_id))

        driver_standing_race_pred = "<{}/pred/at>".format(chosen_base_rdf)
        driver_standing_triples.add("{} {} {} .".format(driver_standing_id, driver_standing_race_pred, race_id))

        driver_code_pred = "<{}/pred/has>".format(chosen_base_rdf)
        driver_triples.add("{} {} {} .".format(driver_id, driver_code_pred, driver_standing_id))

        race_round_pred = "<{}/pred/has>".format(chosen_base_rdf)
        race_triples.add("{} {} {} .".format(race_id, race_round_pred, driver_standing_id))

        #print(row)

    #for i in driver_triples:
    #    print(i)

with open('../datasets/driver_final_standings.csv', 'r') as file:
    file.readline()
    reader = csv.reader(file)

    for row in reader:
        chosen_base_rdf = random.choice(base_rdf_list)

        driver_final_standing_id = "<{}/driver_id/final_standing/{}>".format(chosen_base_rdf, row[0])

        driver_final_standing_season_pred = "<{}/pred/season>".format(chosen_base_rdf)
        driver_final_standing_season = "\"{}\"".format(races_dict[row[1]][0])
        driver_final_standing_triples.add("{} {} {} .".format(driver_final_standing_id, driver_final_standing_season_pred, driver_final_standing_season))

        driver_final_standing_points_pred = "<{}/pred/points>".format(chosen_base_rdf)
        driver_final_standing_points = "\"{}\"".format(row[3])
        driver_final_standing_triples.add("{} {} {} .".format(driver_final_standing_id, driver_final_standing_points_pred, driver_final_standing_points))

        driver_final_standing_position_pred = "<{}/pred/position>".format(chosen_base_rdf)
        driver_final_standing_position = "\"{}\"".format(row[4])
        driver_final_standing_triples.add("{} {} {} .".format(driver_final_standing_id, driver_final_standing_position_pred, driver_final_standing_position))

        driver_final_standing_pred = "<{}/pred/finished_in>".format(chosen_base_rdf)
        driver_triples.add("{} {} {} .".format(driver_id, driver_final_standing_pred, driver_final_standing_id))


    #for i in driver_triples:
    #   print(i)
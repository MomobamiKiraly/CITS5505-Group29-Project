import requests
from datetime import datetime, timezone

ERGAST_BASE_URL = "https://api.jolpi.ca/ergast/f1"


def fetch_teams():
    return [
        {
            "name": "Ferrari",
            "image_url": "  https://media.formula1.com/image/upload/f_auto,c_limit,q_auto,w_1320/content/dam/fom-website/2018-redesign-assets/team%20logos/ferrari.jpg"
        },
        {
            "name": "Red Bull",
            "image_url": "https://media.formula1.com/image/upload/f_auto,c_limit,q_auto,w_1320/content/dam/fom-website/2018-redesign-assets/team%20logos/red%20bull.jpg"
        },
        {
            "name": "Mercedes",
            "image_url": "https://media.formula1.com/image/upload/f_auto,c_limit,q_auto,w_1320/content/dam/fom-website/2018-redesign-assets/team%20logos/mercedes.jpg"
        },
        {
            "name": "McLaren",
            "image_url": "https://media.formula1.com/image/upload/f_auto,c_limit,q_auto,w_1320/content/dam/fom-website/2018-redesign-assets/team%20logos/mclaren.jpg"
        },
        {
            "name": "Aston Martin",
            "image_url": "https://media.formula1.com/image/upload/f_auto,c_limit,q_auto,w_1320/content/dam/fom-website/2018-redesign-assets/team%20logos/aston%20martin.jpg"
        },
        {
            "name": "Alpine",
            "image_url": "https://media.formula1.com/image/upload/f_auto,c_limit,q_auto,w_1320/content/dam/fom-website/2018-redesign-assets/team%20logos/alpine.jpg"
        },
        {
            "name": "Williams",
            "image_url": "https://media.formula1.com/image/upload/f_auto,c_limit,q_auto,w_1320/content/dam/fom-website/2018-redesign-assets/team%20logos/williams.jpg"
        },
        {
            "name": "Racing Bulls",
            "image_url": "https://media.formula1.com/image/upload/f_auto,c_limit,q_auto,w_1320/content/dam/fom-website/2018-redesign-assets/team%20logos/rb.jpg"
        },
        {
            "name": "Kick Sauber",
            "image_url": "https://media.formula1.com/image/upload/f_auto,c_limit,q_auto,w_1320/content/dam/fom-website/2018-redesign-assets/team%20logos/kick%20sauber.jpg"
        },
        {
            "name": "Haas",
            "image_url": "https://media.formula1.com/image/upload/f_auto,c_limit,q_auto,w_1320/content/dam/fom-website/2018-redesign-assets/team%20logos/haas.jpg"
        }
    ]



def get_drivers_by_team():
    return {
    "Ferrari": [
        {
            "name": "Charles Leclerc",
            "image_url": "https://media.formula1.com/image/upload/f_auto,c_limit,q_auto,w_1320/content/dam/fom-website/drivers/2025Drivers/leclerc.jpg"
        },
        {
            "name": "Lewis Hamilton",
            "image_url": "https://media.formula1.com/image/upload/f_auto,c_limit,q_auto,w_1320/content/dam/fom-website/drivers/2025Drivers/hamilton.jpg"
        }
    ],
    "Red Bull": [
        {
            "name": "Max Verstappen",
            "image_url": "https://media.formula1.com/image/upload/f_auto,c_limit,q_auto,w_1320/content/dam/fom-website/drivers/2025Drivers/verstappen.jpg"
        },
        {
            "name": "Liam Lawson",
            "image_url": "https://media.formula1.com/image/upload/f_auto,c_limit,q_auto,w_1320/content/dam/fom-website/drivers/2025Drivers/lawson.jpg"
        }
    ],
    "Mercedes": [
        {
            "name": "George Russell",
            "image_url": "https://media.formula1.com/image/upload/f_auto,c_limit,q_auto,w_1320/content/dam/fom-website/drivers/2025Drivers/russell.jpg"
        },
        {
            "name": "Andrea Kimi Antonelli",
            "image_url": "https://media.formula1.com/image/upload/f_auto,c_limit,q_auto,w_1320/content/dam/fom-website/drivers/2025Drivers/antonelli.jpg"
        }
    ],
    "McLaren": [
        {
            "name": "Lando Norris",
            "image_url": "https://media.formula1.com/image/upload/f_auto,c_limit,q_auto,w_1320/content/dam/fom-website/drivers/2025Drivers/norris.jpg"
        },
        {
            "name": "Oscar Piastri",
            "image_url": "https://media.formula1.com/image/upload/f_auto,c_limit,q_auto,w_1320/content/dam/fom-website/drivers/2025Drivers/piastri.jpg"
        }
    ],
    "Aston Martin": [
        {
            "name": "Fernando Alonso",
            "image_url": "https://media.formula1.com/image/upload/f_auto,c_limit,q_auto,w_1320/content/dam/fom-website/drivers/2025Drivers/alonso.jpg"
        },
        {
            "name": "Lance Stroll",
            "image_url": "https://media.formula1.com/image/upload/f_auto,c_limit,q_auto,w_1320/content/dam/fom-website/drivers/2025Drivers/stroll.jpg"
        }
    ],
    "Alpine": [
        {
            "name": "Pierre Gasly",
            "image_url": "https://media.formula1.com/image/upload/f_auto,c_limit,q_auto,w_1320/content/dam/fom-website/drivers/2025Drivers/gasly.jpg"
        },
        {
            "name": "Jack Doohan",
            "image_url": "https://media.formula1.com/image/upload/f_auto,c_limit,q_auto,w_1320/content/dam/fom-website/drivers/2025Drivers/doohan.jpg"
        }
    ],
    "Haas": [
        {
            "name": "Esteban Ocon",
            "image_url": "https://media.formula1.com/image/upload/f_auto,c_limit,q_auto,w_1320/content/dam/fom-website/drivers/2025Drivers/ocon.jpg"
        },
        {
            "name": "Oliver Bearman",
            "image_url": "https://media.formula1.com/image/upload/f_auto,c_limit,q_auto,w_1320/content/dam/fom-website/drivers/2025Drivers/bearman.jpg"
        }
    ],
    "Racing Bulls": [
        {
            "name": "Yuki Tsunoda",
            "image_url": "https://media.formula1.com/image/upload/f_auto,c_limit,q_auto,w_1320/content/dam/fom-website/drivers/2025Drivers/tsunoda.jpg"
        },
        {
            "name": "Isack Hadjar",
            "image_url": "https://media.formula1.com/image/upload/f_auto,c_limit,q_auto,w_1320/content/dam/fom-website/drivers/2025Drivers/hadjar.jpg"
        }
    ],
    "Kick Sauber": [
        {
            "name": "Nico Hülkenberg",
            "image_url": "https://media.formula1.com/image/upload/f_auto,c_limit,q_auto,w_1320/content/dam/fom-website/drivers/2025Drivers/hulkenberg.jpg"
        },
        {
            "name": "Gabriel Bortoleto",
            "image_url": "https://media.formula1.com/image/upload/f_auto,c_limit,q_auto,w_1320/content/dam/fom-website/drivers/2025Drivers/bortoleto.jpg"
        }
    ],
    "Williams": [
        {
            "name": "Alexander Albon",
            "image_url": "https://media.formula1.com/image/upload/f_auto,c_limit,q_auto,w_1320/content/dam/fom-website/drivers/2025Drivers/albon.jpg"
        },
        {
            "name": "Carlos Sainz",
            "image_url": "https://media.formula1.com/image/upload/f_auto,c_limit,q_auto,w_1320/content/dam/fom-website/drivers/2025Drivers/sainz.jpg"
        }
    ]
}


def get_next_race_name():
    """Fetch the next 5 scheduled races from the 2025 F1 season using Jolpica."""
    try:
        url = "https://api.jolpi.ca/ergast/f1/2025.json"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        print("API response received.")

        races = data.get('MRData', {}).get('RaceTable', {}).get('Races', [])
        print(f"Total races fetched: {len(races)}")

        now_utc = datetime.now(timezone.utc)
        upcoming = []

        for race in races:
            race_date_str = race.get("date")
            race_time_str = race.get("time", "00:00:00Z").replace("Z", "")
            full_datetime_str = f"{race_date_str}T{race_time_str}"

            try:
                race_datetime = datetime.strptime(full_datetime_str, "%Y-%m-%dT%H:%M:%S")
                race_datetime = race_datetime.replace(tzinfo=timezone.utc)
            except ValueError as ve:
                print(f"Date parsing error for race {race.get('raceName')}: {ve}")
                continue

            if race_datetime >= now_utc:
                upcoming.append({
                    "raceName": race.get("raceName"),
                    "circuit": race.get("Circuit", {}).get("circuitName"),
                    "location": f"{race.get('Circuit', {}).get('Location', {}).get('locality')}, {race.get('Circuit', {}).get('Location', {}).get('country')}",
                    "date": race_datetime.strftime("%Y-%m-%d")
                })

        print(f"Upcoming races found: {len(upcoming)}")
        return upcoming[:5]

    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return []
    except Exception as e:
        print(f"Unexpected error: {e}")
        return []



def fetch_team_details(team_name):
    team_id = team_name.lower().replace(" ", "_")
    try:
        team_url = f"https://api.jolpi.ca/ergast/f1/constructors/{team_id}.json"
        standings_url = f"https://api.jolpi.ca/ergast/f1/current/constructorStandings.json"

        team_data = requests.get(team_url).json()
        standings_data = requests.get(standings_url).json()

        team_info = team_data['MRData']['ConstructorTable']['Constructors'][0]
        standings_list = standings_data['MRData']['StandingsTable']['StandingsLists'][0]['ConstructorStandings']

        team_stats = next((t for t in standings_list if t['Constructor']['constructorId'] == team_id), None)
        if team_stats:
            team_info['position'] = team_stats['position']
            team_info['points'] = team_stats['points']
            team_info['wins'] = team_stats['wins']

        return team_info
    except (KeyError, IndexError):
        return None

DRIVER_ID_MAP = {
    "Max Verstappen": "max_verstappen",
    "Sergio Pérez": "perez",
    "Lewis Hamilton": "hamilton",
    "George Russell": "russell",
    "Charles Leclerc": "leclerc",
    "Carlos Sainz": "sainz",
    "Lando Norris": "norris",
    "Oscar Piastri": "piastri",
    "Fernando Alonso": "alonso",
    "Lance Stroll": "stroll",
    "Pierre Gasly": "gasly",
    "Esteban Ocon": "ocon",
    "Valtteri Bottas": "bottas",
    "Andrea Kimi Antonelli": "antonelli",
    "Kevin Magnussen": "magnussen",
    "Nico Hülkenberg": "hulkenberg",
    "Yuki Tsunoda": "tsunoda",
    "Daniel Ricciardo": "ricciardo",
    "Alexander Albon": "albon",
    "Logan Sargeant": "sargeant"
}

def fetch_driver_details(driver_name):
    driver_id = DRIVER_ID_MAP.get(driver_name)
    if not driver_id:
        return None  # Unrecognized driver

    try:
        driver_url = f"https://api.jolpi.ca/ergast/f1/drivers/{driver_id}.json"
        standings_url = f"https://api.jolpi.ca/ergast/f1/current/driverStandings.json"

        driver_data = requests.get(driver_url).json()
        standings_data = requests.get(standings_url).json()

        driver_info = driver_data['MRData']['DriverTable']['Drivers'][0]
        standings_list = standings_data['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings']

        driver_stats = next((d for d in standings_list if d['Driver']['driverId'] == driver_id), None)
        if driver_stats:
            driver_info['position'] = driver_stats['position']
            driver_info['points'] = driver_stats['points']
            driver_info['wins'] = driver_stats['wins']

        return driver_info
    except (KeyError, IndexError):
        return None

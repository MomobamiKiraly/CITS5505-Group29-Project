# app/api_utils.py

import requests

ERGAST_BASE_URL = "https://ergast.com/api/f1"


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
    """Fetch the name of the next scheduled race."""
    try:
        next_race_url = "http://ergast.com/api/f1/current/next.json"
        race_response = requests.get(next_race_url)
        race_response.raise_for_status()
        race_data = race_response.json()
        return race_data['MRData']['RaceTable']['Races'][0]['raceName']
    except (KeyError, IndexError, requests.exceptions.RequestException):
        return None

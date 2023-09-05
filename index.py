from datetime import datetime, timedelta
import requests

usernames = ['Fins', 'GMVallejo']

def process_username(username):
  history_url = f'https://lichess.org/api/user/{username}/rating-history'
  response = requests.get(history_url)
  response.raise_for_status()
  types = response.json()

  print(f'{username}:')
  for type in types:
    if type["name"] == "Rapid" or type["name"] == "Blitz":
      process_type(username, type)
  print()

def process_type(username, type):
  start_365, start_30, start_7 = 0, 0, 0
  games_365, games_30, games_7 = 0, 0, 0

  for point in type["points"]:
    year = point[0]
    month = point[1] + 1
    day = point[2]
    rating = point[3]

    date = datetime.strptime(f'{day}/{month}/{year} 00:00', '%d/%m/%Y %H:%M')
    diff = datetime.now() - date

    if diff.days > 365:
      start_365 = rating
    else:
      games_365 += 1

    if diff.days > 30:
      start_30 = rating
    else:
      games_30 += 1

    if diff.days > 7:
      start_7 = rating
    else:
      games_7 += 1

  if len(type["points"]) > 0:
    point = type["points"][-1]
    year = point[0]
    month = point[1] + 1
    day = point[2]
    rating = point[3]

    date = datetime.strptime(f'{day}/{month}/{year}', '%d/%m/%Y')
    diff = datetime.now() - date
    
    end_365 = 0
    end_30 = 0
    end_7 = 0
    if diff.days <= 365:
      end_365 = rating
    if diff.days <= 30:
      end_30 = rating
    if diff.days <= 7:
      end_7 = rating

    print(f'  {type["name"]} (rating actual): {rating}')
    if end_7 > 0:
      print(f'    7 días:     {end_7 - start_7} ({games_7} juegos, inició con {start_7})')
    else:
      print('    7 días:     N/A (0 juegos)')

    if end_30 > 0:
      print(f'    30 días:    {end_30 - start_30} ({games_30} juegos, inició con {start_30})')
    else:
      print('    30 días:    N/A (0 juegos)')

    if end_365 > 0:
      print(f'    1 año:      {end_365 - start_365} ({games_365} juegos, inició con {start_365})')
    else:
      print('    1 año:      N/A (0 juegos)')

try:
  for username in usernames:
    process_username(username)

except requests.exceptions.RequestException as e:
    print(f'Error: {e}')
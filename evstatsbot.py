import praw
import json
import os
import datetime
import re
from time import sleep
import traceback

useragent = "linux:evstatsbot:v1.0.0 (by /u/magico13)"

reddit = praw.Reddit('evstatsbot', user_agent=useragent)

def load_cars():
  cars = []
  for fname in os.listdir('vehicles'):
    if '.json' in fname:
      with open('vehicles/'+fname, 'r') as f:
        data = f.read()
        if len(data) > 0:
          carset = json.loads(data)
          if 'cars' in carset and len(carset['cars']) > 0:
            cars += carset['cars']
  return cars
  
def format_post(mentioned):
  time = datetime.datetime.utcnow()
  post = 'These are the EVs I have seen mentioned in this thread as of {} UTC:\n\n'.format(time.strftime("%Y-%m-%d %H:%M:%S"))
  post += '|Name|Years|Type|EV Range|Battery|QC Connector|0-60|MSRP|\n'
  post += '|:--|:--|:-:|:-:|:-:|:-:|:-:|:-:|\n'
  for car in sorted(mentioned, key=lambda x: x['title']):
    name = car['title']
    years = '{}-'.format(car['year_start'])
    if 'year_end' in car: years += str(car['year_end'])
    else: years += 'present'
    carType = car['type']
    evRange = '{} miles'.format(car['ev_range'])
    batSize = '{}kwh'.format(car['battery_size'])
    qc = car['qc_type']
    zeroSixty = '{}s'.format(car['zero_sixty'])
    msrp = '${:,}'.format(car['msrp'])
    post += '|{}|{}|{}|{}|{}|{}|{}|{}|\n'.format(name, years, carType, evRange, batSize, qc, zeroSixty, msrp)
  post += '||||||* = optional|||\n'
  post += '  \n'
  post += '^(I\'m a bot and this action was done autonomously.)  \n'
  post += '^(My database is still under construction, so forgive any obviously missing data (esp Tesla variants)^)^. ^( Sorry! I\'m also very US focused *for now*.)  \n'
  post += 'Missing, incorrect, or otherwise invalid data? Open an issue on [github](https://github.com/magico13/evstatsbot) or message /u/magico13.  \n'

  return post

def check_match(text, cars):
  found = []
  text = text.lower()
  for car in cars:
    for regex in car['search_regex']:
      if re.search(regex, text):
        found.append(car)
  return found

def run_against(subreddit, cars):
  for submission in reddit.subreddit(subreddit).new():
    if not submission.locked and (datetime.datetime.utcnow().timestamp() - submission.created_utc) > 3600 and (datetime.datetime.utcnow().timestamp() - submission.created_utc) < 86400:
      # must be not locked, over an hour old, and less than a day old
      #check the self text, then each comment in the submission
      myPost = None
      previouslyFound = []
      print(submission.title)
      foundCars = []
      potentialCars = cars[:]
      found = check_match(submission.selftext, potentialCars)
      for car in found:
        potentialCars.remove(car)
        print(car['title'])
      foundCars += found
      submission.comments.replace_more(limit=0)
      for comment in submission.comments.list():
        #search in the comments
        if comment.author == 'evstatsbot':
          myPost = comment
          previouslyFound = check_match(myPost.body, cars)
        else:
          found = check_match(comment.body, potentialCars)
          for car in found:
            potentialCars.remove(car)
            print(car['title'])
          foundCars += found
          if len(potentialCars) == 0: break
      if len(foundCars) == 0: continue
      post = format_post(foundCars)
      
      if not myPost:
        print()
        submission.reply(post)
      else:
        if not lists_equal(previouslyFound, foundCars):
          print()
          myPost.edit(post)
        else:
          print("No changes")
      
def lists_equal(a, b):
  if len(a) != len(b): return False
  sortA = sorted(a, key=lambda x: x['id'])
  sortB = sorted(b, key=lambda x: x['id'])
  return (sortA == sortB)

cars = load_cars()

for car in cars:
  print(car['title'])
print('{} cars loaded!'.format(len(cars)))

while True:
  try:
    run_against('electricvehicles', cars)
    run_against('evstatsbot', cars)
  except KeyboardInterrupt:
    print('Exiting')
    break
  except e as praw.exceptions.APIException:
    if e.error_type == 'RATELIMIT':
      print('Hit rate limit. Waiting ten minutes. Msg: "{}"'.format(e.message))
      sleep(600)
    else:
      print(str(e))
  except:
    traceback.print_exc()
    pass
  sleep(60)


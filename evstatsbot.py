import praw
import json
import os

useragent = "linux:evstatsbot:v0.1.0 (by /u/magico13)"


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
    post = 'These are the EVs I have seen mentioned in this thread:  \n'
    post += 'Name|Years|Type|EV Range|Battery|QC Connector|0-60|MSRP\n'
    post += ':--|:--|:-:|:-:|:-:|:-:|:-:|:-:\n'
    for car in mentioned:
        name = car['title']
        years = '{}-'.format(car['year_start'])
        if 'year_end' in car: years += str(car['year_end'])
        else: years += 'present'
        carType = car['type']
        evRange = '{} miles'.format(car['ev_range'])
        batSize = '{}kwh'.format(car['battery_size'])
        qc = car['qc_type']
        zeroSixty = '{}s'.format(car['zero_sixty'])
        msrp = '${}'.format(car['msrp'])
        post += '{}|{}|{}|{}|{}|{}|{}|{}\n'.format(name, years, carType, evRange, batSize, qc, zeroSixty, msrp)
    post += '  \n'
    post += 'I\'m a bot and this action was done autonomously.  \n'
    post += 'Missing, incorrect, or otherwise invalid data? Open an issue on [github](https://github.com/magico13/evstatsbot) or message /u/magico13'
    return post

cars = load_cars()

for car in cars:
    print(car['title'])
print('{} cars loaded!'.format(len(cars)))

submission = reddit.submission(id='9dzaie')
#print(submission.selftext)
mentioned = []
lower = submission.selftext.lower()
for car in cars:
    for search in car['search_regex']:
        if search in lower:
            mentioned.append(car)
            break

post = format_post(mentioned)
print(post)
#print(submission.author)
#print(vars(submission))
#print('{}: "{}"'.format(submission.author, submission.selftext))
#submission.comments.replace_more(limit=0)
#for comment in submission.comments.list():
#    print('{}: "{}"'.format(comment.author, comment.body))

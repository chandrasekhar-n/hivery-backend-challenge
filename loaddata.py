import pickle
import redis
import os,json
import itertools
from redis.exceptions import ConnectionError
from config import *
r = None
try:
    r = redis.StrictRedis(host=redis_host, port=redis_port)
except ConnectionError as e:
    print "Redis server is not available or not running port %s. Please update config.py"%redis_port



fruits = ['apple','strawberry', 'orange', 'banana']
vegetables = ['beetroot', 'celery', 'carrot', 'cucumber']


if os.path.isfile('resources/companies.json'):
    with open(os.path.join(os.path.dirname(__file__),'resources/companies.json')) as companies_json:
        companies_data = json.load(companies_json)
        for company in companies_data:
            pickled_object = pickle.dumps(company)
            r.set('company:%s'%company['index'], pickled_object)
            parts = company['company'].split(' ')
            parts.append(company['company'])
            parts = set([x.lower() for x in parts])
            parts = ["%s:%s" % (x.lower(), str(company['index'])) for x in parts]
            # This adds the score
            parts = [(0, x) for x in parts]
            # This flattens the list
            parts = list(itertools.chain.from_iterable(parts))
            r.zadd('autocomplete:company', *parts)



else:
    print "Companies JSON is not loaded to Database. Please check if you have placed the file in path './resources/companies.json'"



if os.path.isfile('resources/people.json'):
    with open(os.path.join(os.path.dirname(__file__),'resources/people.json')) as people_json:
        people_data = json.load(people_json)
        ## finding all unique fav food
        # flat_list = [item for sublist in people_data for item in sublist['favouriteFood'] if 'favouriteFood' in sublist]
        # flat_list = list(dict.fromkeys(flat_list))
        # print flat_list
        for person in people_data:
            person['fruits']=list(set(person['favouriteFood']).intersection(fruits))
            person['vegetables'] = list(set(person['favouriteFood']).intersection(vegetables))
            del person['favouriteFood']
            pickled_object = pickle.dumps(person)
            r.set('person:%s'%person['index'], pickled_object)

            parts = person['name'].split(' ')
            parts.append(person['_id'])
            parts.append(person['name'])
            parts.append(person['email'])
            parts.append(person['email'].split('@')[0])
            parts.extend(person['email'].split('@')[0].split('.'))
            parts = set([x.lower() for x in parts])
            parts = ["%s:%s" % (x.lower(), str(person['index'])) for x in parts]
            # This adds the score
            parts = [(0, x) for x in parts]
            # This flattens the list
            parts = list(itertools.chain.from_iterable(parts))
            r.zadd('autocomplete:person', *parts)


            parts = "%s:%s" % (str(person['company_id']), str(person['index']))
            parts = [(0, x) for x in parts]
            parts = list(itertools.chain.from_iterable(parts))
            r.zadd('companyEmployee',*parts)
else:
    print "People JSON is not loaded to Database. Please check if you have placed the file in path './resources/people.json'"


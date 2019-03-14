from flask import Flask,jsonify,request,make_response
app = Flask(__name__)
import pickle
import redis
from config import *
from redis.exceptions import *

redis_client = None

try:
    redis_client = redis.StrictRedis(host=redis_host, port=redis_port)
except ConnectionError as e:
    print "Redis server is not available or not running port %s. Please update config.py"%redis_port

@app.route("/api/v1/getPeople/<string:query>", methods = ['GET'])
def getPeople(query):
    response = {}
    if query is not None:
        query = query.lower()
        person_withindex = find_person_by_index(query)
        print person_withindex
        personIndices = searchPerson(query)
        if person_withindex is not None:
            people = [{"username": person_withindex['name'], "age": person_withindex['age'], "fruits": person_withindex['fruits'],
                       "vegetables": person_withindex['vegetables']}]
            return make_response(jsonify(people), 200)
        elif len(personIndices) > 0:
            personIndices = set([x.split(':').pop() for x in personIndices])
            people = [find_person_by_index(x) for x in personIndices]
            people = [{"username": x['name'], "age": x['age'], "fruits": x['fruits'],
                       "vegetables": x['vegetables']} for x in people if x]
            return make_response(jsonify(people),200)
        else:
            response['message'] = 'Unable to fetch query parameter, Provide valid person name, email, id or index'
            return make_response(jsonify(response), 404)
    else:
        response['message'] = 'Unable to fetch query parameter, Provide valid person name, email, id or index'
        return make_response(jsonify(response), 404)

@app.route("/api/v1/getMultiPeople", methods = ['POST'])
def getMultiPeople():
    payload = request.get_json()
    response = {}
    personList = []
    commonFriends = []
    if len(payload) ==2:
        for person in payload:
            personIndices = searchPerson(person)
            if len(personIndices)>0:
                personIndices = set([x.split(':').pop() for x in personIndices])
                people = [find_person_by_index(x) for x in personIndices]
                people = people[0]
                personList.append({'name':people['name'],'age':people['age'],'address':people['address'],'phone':people['phone'],'friends':people['friends']})
        if len(personList)==2:
            commonFriends = [i['index'] for i in personList[0]['friends'] for j in personList[1]['friends'] if i['index'] == j['index']]
            commonFriends = [ find_person_by_index(friend) for friend in commonFriends]
            commonFriends = [ {'name':friend['name'],'age':friend['age'],'address':friend['address'],'phone':friend['phone']} for friend in commonFriends if not friend['has_died'] and friend['eyeColor'] == 'brown']

            for person in personList:
                if 'friends' in person:
                    del person['friends']

            response['people'] = personList
            response['commonFriends'] = commonFriends
            return make_response(jsonify(response),200)
        else:
            response['message'] = 'Unable to fetch People %s, Provide valid name or index'%str(payload)
            return make_response(jsonify(response),404)
    else:
        response['message'] = 'This API takes exactly two names for searching'
        return make_response(jsonify(response),404)


@app.route("/api/v1/getCompanyEmployees/<string:query>", methods = ['GET'])
def getCompany(query):
    response = {}
    employees=[]
    if query is not None:
        query = query.lower()
        companyIndices = searchCompany(query)
        company_withindex = find_company_by_index(query)
        print company_withindex
        if company_withindex is not None:
            employeeIndeces = getEmployeeIndeces(str(company_withindex['index']))
            employeeIndeces = set([x.split(':').pop() for x in employeeIndeces])
            employees = [find_person_by_index(x) for x in employeeIndeces]
            return make_response(jsonify(employees), 200)
        elif len(companyIndices) > 0:
            companyIndices = set([x.split(':').pop() for x in companyIndices])
            companies = [find_company_by_index(x) for x in companyIndices]
            for company in companies:
                employeeIndeces =  getEmployeeIndeces(str(company['index']))
                employeeIndeces = set([x.split(':').pop() for x in employeeIndeces])
                employees = [find_person_by_index(x) for x in employeeIndeces]
            return make_response(jsonify(employees), 200)
        else:
            response['message'] = 'Unable to fetch company, Provide valid company name or index'
            return make_response(jsonify(response), 404)
    else:
        response['message'] = 'Unable to fetch company, Provide valid company or index'
        return make_response(jsonify(response), 404)


def find_person_by_index(index):
    data = redis_client.get('person:%s'%index)
    if not data:
        return None
    return pickle.loads(data)

def find_company_by_index(index):
    data = redis_client.get('company:%s'%index)
    if not data:
        return None
    return pickle.loads(data)

def searchPerson(query):
    return redis_client.zrangebylex('autocomplete:person', '[%s' % query, u"[%s\xFF" % query[:-1], start=0, num=10)

def searchCompany(query):
    return redis_client.zrangebylex('autocomplete:company', '[%s' % query, u"[%s\xFF" % query[:-1], start=0, num=10)

def getEmployeeIndeces(companyIndex):
    return redis_client.zrangebylex('companyEmployee', '[%s' % companyIndex, u"[%s\xFF" % companyIndex[:-1], start=0, num=10)

if __name__ == '__main__':
    app.run()
# Paranuara Challenge
Paranuara is a class-m planet. Those types of planets can support human life, for that reason the president of the Checktoporov decides to send some people to colonise this new planet and
reduce the number of people in their own country. After 10 years, the new president wants to know how the new colony is growing, and wants some information about his citizens. Hence he hired you to build a rest API to provide the desired information.

The government from Paranuara will provide you two json files (located at resource folder) which will provide information about all the citizens in Paranuara (name, age, friends list, fruits and vegetables they like to eat...) and all founded companies on that planet.
Unfortunately, the systems are not that evolved yet, thus you need to clean and organise the data before use.
For example, instead of providing a list of fruits and vegetables their citizens like, they are providing a list of favourite food, and you will need to split that list (please, check below the options for fruits and vegetables).

## New Features
New API's must provide these end points:
- Given a company, the API will return all their employees. 
- Given 2 people, provide their information (Name, Age, Address, phone) and the list of their friends in common which have brown eyes and are still alive.
- Given 1 people, provide a list of fruits and vegetables they like. This endpoint must respect this interface for the output: `{"username": "Ahi", "age": "30", "fruits": ["banana", "apple"], "vegetables": ["beetroot", "lettuce"]}`

## Technical stack

This solutions uses Basic Python Flask and Redis DB. Following commands from Redis has been used to store and retrieve data.
`SET, GET, ZADD, ZRANGEBYLEX`

## Assumptions
- Based on test data, Current API treats that there are limited vegetables and fruits available on Paranuara and they are as follows.

```python
fruits = ['apple','strawberry', 'orange', 'banana']
vegetables = ['beetroot', 'celery', 'carrot', 'cucumber']
```

## Setup

- Server Setup
  - This application runs on Python 2.7
  - create virtual env and run the server with below commands
```bash
git pull https://github.com/chandrasekhar-n/hivery-backend-challenge.git
virtualenv hivery
source hivery/bin/activate
pip install -r requirements.txt
export FLASK_APP='paranuara/app.py'
flask run
```
- Data setup
  - Make sure Redis is running on port 6379 and companies.json & people.json are in the path `./resources/`
  - To load data to Redis server run the below command ```python loaddata.py```
 
- Running tests
  - Make sure redis server is running
  - Run tests.py using `py.test`  

## API Specification

- Please use below URL's to test the API's

| API URL | HTTP Method |Description| Input | 
| --- | --- | --- | ---- | 
|  /api/v1/getPeople/param1| GET | Retrieve user data when id or other info of user given | param1:`index/Name/email/ID` of person | 
| /api/v1/getMultiPeople | POST | Retrieve information about 2 people when id or other info of users given | JSON array of `index/name/email/ID` eg: `['camella','etta']`|
| /api/v1/getCompanyEmployees/param1| GET | Retrieve employees working in a company | param1:`index/name`|





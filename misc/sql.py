__author__ = 'azhar'
import simplejson as json

def get_countries_sql():
    f = open("countries").read().split("\n")
    for ab in f:
        query = """INSERT into core_countries(country_name)VALUES("{0}");""".format(ab)
        print query

def get_cities_sql():
    od = open('cities.json', "r+").read()
    data = json.loads(od)
    return data['United States']

for ab in get_cities_sql():
        query = """INSERT into core_cities(country_id, city_name)VALUES({0},"{1}");""".format(188,ab.encode('utf-8'))
        o = open("cities.txt", "a+").write(query)
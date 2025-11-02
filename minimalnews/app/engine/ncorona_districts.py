import requests


def corona_district(id):
    url = "https://data.nepalcorona.info/api/v1/districts/"+id
    r = requests.get(url)

    c = r.json()  # convert into dict

    district_name = c['title']
    print(district_name)
    print('Total number of cases is {}.'.format(
        c['covid_summary']['cases']))
    print('Total number of active cases is {}.'.format(
        c['covid_summary']['active']))
    print('Total number of recovered cases is {}.'.format(
        c['covid_summary']['recovered']))
    print('Total number of death is {}.'.format(
        c['covid_summary']['death']))


def get_district_id(district_name):
    url = "https://data.nepalcorona.info/api/v1/districts"
    r = requests.get(url)
    d = r.json()

    for i in range(77):
        if (d[i]['title']).upper() == district_name.upper():
            return d[i]['id']


district = input('Enter the name of the district:')
d_id = get_district_id(district)
corona_district(str(d_id))

import requests

url = 'https://nepalcorona.info/api/v1/data/nepal'
r = requests.get(url)

jt = r.json()  # convert into dict

positive_test = jt['tested_positive']
negative_test = jt['tested_negative']
total_test = jt['tested_total']
recovered = jt['recovered']
deaths = jt['deaths']
updated_at = jt['updated_at']
rdt = jt['tested_rdt']


print('Total tests conducted: {}'.format(total_test))
print('Total RDT tests: {}'.format(rdt))
print('Total number of positive cases: {}'.format(positive_test))
print('Total number of negative cases: {}'.format(negative_test))
print('Number of recovered patients: {}'.format(recovered))
print('Total deaths: {}'.format(deaths))
print('Last updated at: {}'.format(updated_at))

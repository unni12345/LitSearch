import requests
from bs4 import BeautifulSoup

def get_pm_ids():
	partial_url = "https://pubmed.ncbi.nlm.nih.gov/trending/?page="
	pm_ids = []
	#iteration over each page
	for i in range(1,11):
		url = partial_url + str(i)
		response = requests.get(url)
		soup = BeautifulSoup(response.content, 'html.parser')
		spans = soup.findAll('span', class_="docsum-pmid")
		for span in spans:
			pm_ids.append(span.text.strip())
	return pm_ids


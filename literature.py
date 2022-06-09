import requests
from bs4 import BeautifulSoup
import pm_ids
import json
import pandas as pd
import database
import psycopg2

class Literature:
	def __init__(self):
		self.arr = []
		self.headers  = ["pm_id","title", "abstract", "publication_types", "mesh_terms", "substances"]
		self.ids = pm_ids.get_pm_ids()
		self.conn = psycopg2.connect(database = "postgres", user = "postgres", password = "pass123", 
			host = "127.0.0.1", port = "5432")

	def get_title(self, soup):
		return soup.title.text.strip()

	def get_abstract(self, soup):
		abstract_text = soup.find('div', id="abstract")
		if abstract_text:
			return abstract_text.text.strip()
		return

	def get_publication_types(self, soup):
		types = soup.find('div', id="publication-types")
		publication_types = {}

		if types is not None:
			for child in types.children:
				if child.name == "ul":
					for grand_child in child:
						if grand_child.name == "li" and grand_child.div.button.text.strip():
							publication_types[grand_child.div.button.text.strip()] = True
		return publication_types

	def get_mesh_terms(self, soup):
		types = soup.find('div', id="mesh-terms")
		mesh_terms = {}

		if types is not None:
			for child in types.children:
				if child.name == "ul":
					for grand_child in child:
						if grand_child.name == "li" and grand_child.div.button.text.strip():
							mesh_terms[grand_child.div.button.text.strip()] = True
		return mesh_terms

	def get_substances(self, soup):
		types = soup.find('div', id="substances")
		substances = {}

		if types is not None:
			for child in types.children:
				if child.name == "ul":
					for grand_child in child:
						if grand_child.name == "li" and grand_child.div.button.text.strip():
							substances[grand_child.div.button.text.strip()] =  True
		return substances

	def close_connection(self):
		self.conn.close()

	def start(self):
		# looping through the 100 pm_ids scrapped
		for pm_id in self.ids:
			print(pm_id, " pm_id started")

			url = "https://pubmed.ncbi.nlm.nih.gov/" + str(pm_id)
			response = requests.get(url)
			soup = BeautifulSoup(response.content, 'html.parser')

			#title
			title = self.get_title(soup)

			#abstract
			abstract = self.get_abstract(soup)

			#publication types
			publication_types = self.get_publication_types(soup)

			#mesh types
			mesh_terms = self.get_mesh_terms(soup)

			#substances
			substances = self.get_substances(soup)

			row = [pm_id, title, abstract, publication_types, mesh_terms, substances]

			#db write
			database.add_row_to_literature(self.conn,row)

			self.arr.append(row)
			print(pm_id, " pm_id finished")

		# write to csv
		pd.DataFrame(self.arr, columns = self.headers).to_csv('data.csv')

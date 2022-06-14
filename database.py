import json
import nlp_service

def to_json(response):
	mydict = {}
	for row in response:
		entities = ""
		if row[2] is not None:
			entities = nlp_service.get_ner_response(row[2])
		mydict[row[0]] = {"title":row[1],"abstract":row[2],"publication_types":row[3], "mesh_terms": row[4], "substances": row[5], "entities": entities}
	return json.dumps(mydict, indent=2, sort_keys=True)


def add_row_to_literature(conn, row):
	cur = conn.cursor()
	cur.execute('SELECT PM_ID FROM Literature where PM_ID = (%s)', (row[0],))
	exist = cur.fetchone()
	print("exist is", exist)
	if not exist:
		cur.execute("INSERT INTO Literature (PM_ID, TITLE, ABSTRACT, PUBLICATION_TYPES, MESH_TERMS, SUBSTANCES) VALUES (%s,%s,%s,%s,%s,%s)", (row[0], row[1], row[2], json.dumps(row[3]), json.dumps(row[4]), json.dumps(row[5])))
		print("row added")
	else:
		print("row to be updated")
	conn.commit()

def get_filtered_on_publication_types(conn, val):
	cur = conn.cursor()
	cur.execute('SELECT * FROM Literature where publication_types ? (%s)', (val,))
	return(to_json(cur.fetchall()))

def get_filtered_on_mesh_terms(conn, val):
	cur = conn.cursor()
	cur.execute('SELECT * FROM Literature where mesh_terms ? (%s)', (val,))
	return(to_json(cur.fetchall()))

def get_filtered_on_substances(conn, val):
	cur = conn.cursor()
	cur.execute('SELECT * FROM Literature where substances ? (%s)', (val,))
	return(to_json(cur.fetchall()))

def update_count(conn, word, new_count):
	cur = conn.cursor()
	cur.execute('UPDATE SEARCH_COUNT SET count = %s WHERE WORD = (%s)', (new_count,word))
	conn.commit()

def add_count(conn, word):
	cur = conn.cursor()
	cur.execute('INSERT INTO SEARCH_COUNT (word, count) VALUES (%s,%s)',(word, 1))
	conn.commit()

def handle_word_count(conn, word):
	print("inside handle_word_count")
	cur = conn.cursor()
	cur.execute('SELECT count from SEARCH_COUNT WHERE word = (%s);', (word,))
	resp = cur.fetchone()
	if resp is not None:
		(current_count, ) = resp
		print("update count in progress")
		update_count(conn, word, current_count + 1)
	else:
		print("add count in progress")
		add_count(conn, word)
	return(True)

def search(conn, word):
	cur = conn.cursor()
	cur.execute('SELECT * FROM Literature WHERE to_tsvector(abstract) @@ to_tsquery(%s)', (word,))
	print("search in progress")
	resp = cur.fetchall()
	if (resp):
		handle_word_count(conn, word)
	return(to_json(resp))

def frequent_5(conn):
	cur = conn.cursor()
	cur.execute('SELECT word, count FROM SEARCH_COUNT ORDER BY count DESC LIMIT 5;')
	resp = cur.fetchall()
	response = {}
	for res in resp:
		(key, value) = res
		response[key] = value

	return (json.dumps(response, indent=2, sort_keys=True))

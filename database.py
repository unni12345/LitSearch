import json

def to_json(response):
	mydict = {}
	for row in response:
		 mydict[row[0]] = {"title":row[1],"abstract":row[2],"publication_types":row[3], "mesh_terms": row[4], "substances": row[5]}
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


# response in JSON form

# for row in result:
    # mydict.add(row[0],({"name":row[1],"email":row[2],"phone":row[3]}))

# select id, title, description, published_at FROM video WHERE to_tsvector(title || ' ' || description) @@ to_tsquery(term)

# ALTER TABLE LITERATURE ADD COLUMN ts tsvector GENERATED ALWAYS AS (to_tsvector('english', abstract)) STORED;

# CREATE INDEX ts_idx ON LITERATURE USING GIN (ts);

# SELECT PM_ID FROM LITERATURE WHERE ts @@ to_tsquery('english', 'tornado');


# FUTURE
# SELECT to_tsvector('The quick brown fox jumped over the lazy dog')  
#     @@ to_tsquery('fox');

# CREATE TABLE SEARCH_COUNT(word CHARACTER(50) PRIMARY KEY     NOT NULL, COUNT           BIGINT);

# "UPDATE Literature SET (PM_ID, TITLE, ABSTRACT, PUBLICATION_TYPES, MESH_TERMS, SUBSTANCES) VALUES (%s,%s,%s,%s,%s,%s) WHERE PM_ID IS %s", (row[0], row[1], row[2], row[3], row[4], row[5], row[0]))

# create_literature_table()

# SELECT * FROM Literature;

# CREATE TABLE Literature(PM_ID CHARACTER(8) PRIMARY KEY     NOT NULL,TITLE           TEXT    NOT NULL,ABSTRACT        TEXT,  ,PUBLICATION_TYPES         JSONB,MESH_TERMS         JSONB,SUBSTANCES         JSONB);

# ALTER TABLE ONLY Literature ADD COLUMN "created_at" TIMESTAMP DEFAULT NOW();
# ALTER TABLE ONLY Literature ADD COLUMN "id" TIMESTAMP DEFAULT NOW();

# INSERT INTO Literature (PM_ID, TITLE, ABSTRACT, PUBLICATION_TYPES, MESH_TERMS, SUBSTANCES) VALUES (row[0], row[1], row[2], row[3], row[4], row[5])
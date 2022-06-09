import database
from literature import Literature

# script for testing

litsearch = Literature()
litsearch.start()

filter_ = 'Humans'
resp_ = database.get_filtered_on_mesh_terms(litsearch.conn, filter_)
print("Humans ->", resp_)

words = ['pathology', 'metabolism', 'chemotherapy', 'virus', 'patient']
for word in words:
	resp = database.search(litsearch.conn, word)
	print(word, " ->", resp)

print("frequent 5 ->", database.frequent_5(litsearch.conn))


# db close
litsearch.close_connection()
print("connection closed")
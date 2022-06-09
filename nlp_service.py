import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag

def get_ner_response(text):
	tokens = nltk.word_tokenize(text)

	# remove stop words
	stop_words = set(stopwords.words('english'))

	filtered_tokens = [w for w in tokens if not w.lower() in stop_words]

	tagged = nltk.pos_tag(filtered_tokens)
	entities = nltk.chunk.ne_chunk(tagged)
	return(entities)

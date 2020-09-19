import nltk
nltk.download('wordnet')

# <collection id="popular" name="Popular packages">
#   <item ref="cmudict" />
#   <item ref="gazetteers" />
#   <item ref="genesis" />
#   <item ref="gutenberg" />
#   <item ref="inaugural" />
#   <item ref="movie_reviews" />
#   <item ref="names" />
#   <item ref="shakespeare" />
#   <item ref="stopwords" />
#   <item ref="treebank" />
#   <item ref="Twitter_samples" />
#   <item ref="omw" />
#   <item ref="wordnet" />
#   <item ref="wordnet_ic" />
#   <item ref="words" />
#   <item ref="maxent_ne_chunker" />
#   <item ref="punkt" />
#   <item ref="Snowball_data" />
#   <item ref="averaged_perceptron_tagger" />
# </collection>


#identificação dos tokens
text = "Alguns animais sabem comunicar com gestos."
tokenizer = nltk.tokenize.TreebankWordTokenizer()
tokens = tokenizer.tokenize(text)
print(tokens)



#stemming
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
ps = PorterStemmer()
words = ["program", "programs", "programer", "programing", "programers"]
for w in words:
    print(w, " : ", ps.stem(w))



#lemma
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
print("rocks :", lemmatizer.lemmatize("rocks"))
print("corpora :", lemmatizer.lemmatize("corpora"))
print("cars :", lemmatizer.lemmatize("cars"))
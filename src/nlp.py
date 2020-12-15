import nltk
import gensim
import gensim.downloader as api
from nltk.tokenize import word_tokenize
# from nltk.corpus import stopwords
import string

clue = "mehmet is sexy"
word_vectors = api.load("glove-wiki-gigaword-50")

stopwords = nltk.download('stopwords')


stop = stopwords.words('english') + list(string.punctuation)
guess_length = 10  # Length of word required for our crossword
topn = 100  # No. of words to be returned by Gensim's most_similar()

pos_words = [word for word in word_tokenize(clue.lower()) if word not in stop]

probable_guesses = [word for word in word_vectors.most_similar(
    positive=pos_words, topn=topn) if len(word[0]) == guess_length]

print(probable_guesses)

# class NLP:
#     def __init__(self):
#         //

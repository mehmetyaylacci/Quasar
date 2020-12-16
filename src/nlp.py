# import gensim
# import gensim.downloader as api
# from nltk.tokenize import word_tokenize
# from nltk.corpus import stopwords
# import string
# import nltk
import json
from urllib import request

lookup = "series"
url = "https://api.datamuse.com/words?rel_gen=" + lookup + "&max=999"
response = request.urlopen(url)
data = json.loads(response.read())

res = []
for i in data:
  res.append(i["word"])
  if i["word"] == "maths":
    print("siktik")

print(res)
# print(res)

# from datamuse import datamuse

# api = datamuse.Datamuse()
# pipi = api.words(rel_ml='bashful')
# print(pipi)
'''
for s in word_sent:
  for word in s:
    if word not in self._stopwords:
      freq[word] += 1
'''

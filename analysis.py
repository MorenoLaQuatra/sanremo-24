import os
import glob
import random
import spacy
import matplotlib.pyplot as plt
from string import punctuation
from collections import Counter
from wordcloud import WordCloud

spacy_model_name = "it_core_news_sm"
root = "songs_text/"

# Step 1: List all text files in the directory
files = glob.glob(root + "*.txt")
print("Number of files:", len(files))

# Step 2: Read all texts from the files
texts = []
for file in files:
    with open(file, "r") as f:
        texts.append(f.read().replace("’", "'").replace("\n", " "))

# Step 3: Load Italian language model for tokenization
nlp = spacy.load(spacy_model_name)

# Step 4: Tokenize Italian texts and remove punctuation, stopwords, and lowercase the tokens
tokens = []
for text in texts:
    ts = [token.text.lower() for token in nlp(text) if token.text not in punctuation]
    ts = [t for t in ts if not nlp.vocab[t].is_stop]
    tokens.append(ts)

# Step 5: Flatten the list of tokens
tokens = [token for sublist in tokens for token in sublist]

# Step 6: Remove single or 2-letter words
tokens = [token for token in tokens if len(token) > 3]

# Step 7: Shuffle tokens
random.shuffle(tokens)

# Step 8: Calculate word count
word_count = sum([len(text) for text in tokens])
print("Word count:", word_count)

# Step 9: Print most common words
c = Counter(tokens)
print(c.most_common(10))

# Step 10: Generate and display word cloud
wordcloud = WordCloud(width=800, height=400, max_font_size=100, background_color="white").generate(" ".join(tokens))
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.savefig("wordcloud-sanremo-24.png")

print("Done!")
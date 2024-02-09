from transformers import pipeline, AutoTokenizer
import os, glob
import matplotlib.pyplot as plt

model_tag = "MilaNLProc/feel-it-italian-emotion"

text_classifier = pipeline("text-classification", model=model_tag, tokenizer=model_tag)
tokenizer = AutoTokenizer.from_pretrained(model_tag)

files = glob.glob("songs_text/*.txt")
song_names = []
labels = []
for file in files:
    f = open(file, "r")
    text = f.read().replace("’", "'").replace("\n", " ")
    f.close()
    
    # take the first 512 tokens
    tokens = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=256)
    text = tokenizer.decode(tokens["input_ids"][0])
    
    c = text_classifier(text)
    labels.append(c[0]["label"])
    
    song_name = os.path.basename(file).replace(".txt", "")
    song_name = song_name.replace("_", " ")
    song_name = song_name.replace("-", " - ")
    song_name = " ".join([word.capitalize() for word in song_name.split()])
    song_names.append(song_name)
    
# print the results
for i in range(len(song_names)):
    print(f"{labels[i]}: {song_names[i]}")
    
# save as TSV file
with open("emotion-distribution-sanremo-24.tsv", "w") as f:
    f.write("song\temotion\n")
    for i in range(len(song_names)):
        f.write(f"{song_names[i]}\t{labels[i]}\n")
    
    

# Define colors for each emotion label
emotion_colors = {
    "anger": "red",
    "fear": "orange",
    "joy": "green",
    "sadness": "blue",
}

# Plotting
emotion_counts = {label: labels.count(label) for label in set(labels)}

# Plot the bar graph
plt.figure(figsize=(10, 6))
colors = ['blue', 'orange', 'green', 'red', 'purple']
plt.bar(emotion_counts.keys(), emotion_counts.values(), color=colors)
plt.xlabel('Emotion')
plt.ylabel('Frequency')
plt.title('Emotion Distribution in Songs')
plt.xticks(rotation=45)
plt.tight_layout()

# Show plot
plt.savefig("emotion-distribution-sanremo-24.png")
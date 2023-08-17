from urllib.parse import urlparse
from collections import Counter
from data_analysis import DataAnalysis
import re


# Function to tokenize a path
def tokenize(path):
    return re.findall(r'\w+', path.lower())


da = DataAnalysis()

# Read URLs from file
with open('urls.txt', 'r') as file:
    urls = [line.strip() for line in file]

# Counter for words and directories
word_counter = Counter()
directory_counter = Counter()

# Iterate through the URLs
for url in urls:
    parsed_url = urlparse(url)
    path = parsed_url.path
    directories = path.split('/')

    # Count directories
    for directory in directories:
        if directory:
            directory_counter[directory] += 1

    # Tokenize and count words
    words = tokenize(path)
    word_counter.update(words)

# Top 10 common words
common_words = word_counter.most_common(10)
print("Top 10 common words:", common_words)

# Top 10 common directories
common_directories = directory_counter.most_common(10)
print("Top 10 common directories:", common_directories)

da.visualize_data(common_words, common_directories)
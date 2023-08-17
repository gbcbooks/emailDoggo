import sqlite3
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
from joblib import load
import re
import matplotlib.pyplot as plt

from sklearn.feature_extraction.text import TfidfVectorizer


def plot_bar(data, title, xlabel, ylabel):
    keys = [item[0] for item in data]
    values = [item[1] for item in data]
    plt.bar(keys, values)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=45, ha='right')
    plt.show()


class DataAnalysis:
    def __init__(self, db_file='web_crawler.db'):
        self.db_file = db_file

        # Function to plot a bar chart

    def visualize_data(self, common_words, common_directories):
        # Plot Common Words
        plot_bar(common_words, 'Top Common Words', 'Words', 'Frequency')

        # Plot common directories
        plot_bar(common_directories, 'Top Common Directories', 'Directories', 'Frequency')

    def get_all_content(self):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute("SELECT url, content FROM urls")
        results = cursor.fetchall()
        conn.close()
        return results

    def load_classifier(self, file_name='trained_classifier.joblib'):
        loaded_classifier = load(file_name)
        print(f"Trained classifier loaded from {file_name}.")
        return loaded_classifier

    def extract_features(self, urls, contents):
        url_vectorizer = TfidfVectorizer(max_features=100)
        content_vectorizer = TfidfVectorizer(max_features=1000)

        url_features = url_vectorizer.fit_transform(urls)
        content_features = content_vectorizer.fit_transform(contents)

        return url_features, content_features

    def load_data(self, db_file='web_crawler.db'):
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        # Join emails and urls tables to get positive examples
        query = '''
        SELECT u.url, u.content, 1 AS label
        FROM urls u
        JOIN emails e ON u.url = e.url
        UNION ALL
        SELECT u.url, u.content, 0 AS label
        FROM urls u
        LEFT JOIN emails e ON u.url = e.url
        WHERE e.url IS NULL
        '''

        cursor.execute(query)
        results = cursor.fetchall()
        conn.close()

        urls = [row[0] for row in results]
        contents = [row[1] for row in results]
        labels = [row[2] for row in results]

        return urls, contents, labels

    def analyze_content(self):
        # Retrieve all content
        contents = self.get_all_content()

        # Iterate through the contents
        for url, html_content in contents:
            # Extract text content
            soup = BeautifulSoup(html_content, 'html.parser')
            text_content = soup.get_text()

            # Tokenize text
            tokens = word_tokenize(text_content)

            # Analyze word frequency (excluding email addresses)
            words = [word for word in tokens if not re.match(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}', word)]
            freq_dist = FreqDist(words)
            freq_dist.plot(30)  # Plot the 30 most common words
            # ... Additional NLP analysis ...


# Usage example:
if __name__ == '__main__':
    data_analysis = DataAnalysis()
    data_analysis.analyze_content()

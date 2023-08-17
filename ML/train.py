from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from scipy.sparse import hstack
from data_analysis import DataAnalysis
from joblib import dump

da = DataAnalysis()


def train():
    urls, contents, labels = da.load_data()
    url_features, content_features = da.extract_features(urls, contents)

    # Combine URL and content features
    X = hstack([url_features, content_features])
    y = labels

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train classifier
    classifier = RandomForestClassifier(random_state=42)
    classifier.fit(X_train, y_train)

    # Evaluate classifier
    y_pred = classifier.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {accuracy}")

    # Assuming classifier is your trained model
    file_name = 'trained_classifier.joblib'
    dump(classifier, file_name)



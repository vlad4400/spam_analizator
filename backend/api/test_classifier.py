from spam_classifier import SpamClassifier

if __name__ == "__main__":
    clf = SpamClassifier(csv_path="spam_NLP.csv")
    clf.train()

    sample_text = "Give me your bank account number to get a million dollars!"
    result = clf.predict(sample_text)
    print("SPAM" if result == 1 else "HAM")

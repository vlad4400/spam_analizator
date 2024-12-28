import re
import numpy as np
import pandas as pd

# NLTK - tokenizacja, stopwords, lematyzacja
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Gensim - do Word2Vec
from gensim.models import Word2Vec

# Scikit-learn - kNN
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score

# Upewnij się, że wykonałeś:
# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('wordnet')

class SpamClassifier:
    def __init__(self, csv_path: str):
        """
        :param csv_path: ścieżka do pliku 'spam_NLP.csv'
                         zakładamy, że kolumny to [CATEGORY, MESSAGE, ...]
                         CATEGORY: 1 = spam, 0 = nie-spam
        """
        self.csv_path = csv_path

        # Zasoby / obiekty wypełnione po train()
        self.model_w2v = None           # Word2Vec
        self.classifier = None          # KNeighborsClassifier
        self.vector_size = 100          # wymiar wektorów Word2Vec
        self.stop_words = set(stopwords.words('english'))
        self.lemmatizer = WordNetLemmatizer()

    def load_data(self):
        """
        Wczytuje CSV, usuwa wiersze z pustą kolumną 'MESSAGE'.
        Zwraca DataFrame z kolumnami [CATEGORY, MESSAGE].
        """
        df = pd.read_csv(self.csv_path)
        df.dropna(subset=['MESSAGE'], inplace=True)
        return df

    def preprocess_text(self, text: str) -> list:
        """
        - Małe litery
        - Usunięcie znaków spoza a-z0-9 spację
        - Tokenizacja NLTK (word_tokenize)
        - Usunięcie stopwords
        - Lematyzacja
        Zwraca listę tokenów.
        """
        text = text.lower()
        text = re.sub(r'[^a-z0-9 ]', '', text)  # wywalamy dziwne znaki

        tokens = word_tokenize(text)
        clean_tokens = []
        for tok in tokens:
            if tok not in self.stop_words:
                lemma = self.lemmatizer.lemmatize(tok)
                clean_tokens.append(lemma)
        return clean_tokens

    def get_mean_vector(self, tokens: list) -> np.ndarray:
        """
        Zwraca średni wektor (mean embedding) dla listy tokenów
        za pomocą self.model_w2v.
        Jeśli brak tokenów / brak wektorów, zwraca wektor zerowy.
        """
        if not tokens:
            return np.zeros(self.vector_size)

        vectors = []
        for tok in tokens:
            if tok in self.model_w2v.wv.key_to_index:
                vectors.append(self.model_w2v.wv[tok])

        if len(vectors) == 0:
            return np.zeros(self.vector_size)

        return np.mean(vectors, axis=0)

    def train(self):
        """
        1) Wczytuje dane z CSV.
        2) Przetwarza każdą wiadomość -> listę tokenów.
        3) Trenuje Word2Vec na wszystkich tokenach.
        4) Tworzy wektory (średnie) dla każdej wiadomości.
        5) Trenuje kNN.
        6) Wyświetla accuracy na zbiorze testowym.
        """
        df = self.load_data()

        # Preprocessing - kolumna tokens
        df['tokens'] = df['MESSAGE'].apply(self.preprocess_text)

        # Trening Word2Vec - na wszystkich tokenach
        all_tokens = df['tokens'].tolist()  # lista list
        self.model_w2v = Word2Vec(
            sentences=all_tokens,
            vector_size=self.vector_size,
            epochs=15,
            min_count=1
        )

        # Tworzymy wektory - po 1 wektorze na wiadomość (mean embedding)
        X_vectors = []
        for toks in df['tokens']:
            vec = self.get_mean_vector(toks)
            X_vectors.append(vec)
        X_vectors = np.array(X_vectors)

        y = df['CATEGORY'].values  # 0 lub 1

        # Podział train/test
        X_train, X_test, y_train, y_test = train_test_split(
            X_vectors, y, test_size=0.2, random_state=42
        )

        # kNN
        self.classifier = KNeighborsClassifier(n_neighbors=5)
        self.classifier.fit(X_train, y_train)

        # Ewaluacja
        y_pred = self.classifier.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        print(f"Accuracy (kNN + Word2Vec) = {acc:.3f}")

    def predict(self, text: str) -> int:
        """
        Zamienia podany text na mean embedding i zwraca 1 (spam) lub 0 (ham).
        """
        if self.model_w2v is None or self.classifier is None:
            raise ValueError("Najpierw wywołaj 'train()'!")

        tokens = self.preprocess_text(text)
        vec = self.get_mean_vector(tokens)
        pred = self.classifier.predict([vec])[0]
        return pred

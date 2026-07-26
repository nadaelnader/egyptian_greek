# -*- coding: utf-8 -*-
"""
Preprocessing module.

Loads the Egyptian/Greek myths dataset from Excel and provides
text-cleaning utilities used for BM25 and embedding-based retrieval.
"""

import os
import re
import string

import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

# ---------------------------------
# NLTK setup
# ---------------------------------
# Make sure the required NLTK data packages are available.
for package in ("punkt", "punkt_tab", "stopwords", "wordnet"):
    try:
        nltk.data.find(f"tokenizers/{package}")
    except LookupError:
        try:
            nltk.download(package, quiet=True)
        except Exception:
            pass

lemmatizer = WordNetLemmatizer()
translator = str.maketrans("", "", string.punctuation)

# Important words that should never be removed
protected_words = {
    "not", "no", "nor", "never",
    "egyptian", "greek",
    "god", "goddess",
    "pharaoh", "king",
    "queen", "myth",
    "historical", "history",
}

try:
    stop_words = set(stopwords.words("english"))
except LookupError:
    stop_words = {
        "the", "is", "and", "a", "an",
        "of", "to", "in", "for", "with",
        "on", "at", "by", "from",
    }


def safe_word_tokenize(text):
    try:
        return word_tokenize(text)
    except LookupError:
        return re.findall(r"\b[\w'-]+\b", text)


def safe_lemmatize(token):
    token = token.lower()
    try:
        return lemmatizer.lemmatize(token)
    except LookupError:
        return token


# ---------------------------------
# BM25 Preprocessing
# ---------------------------------
def preprocess_for_bm25(text):
    if text is None:
        return ""
    text = str(text).lower()
    # Remove URLs
    text = re.sub(r"http\S+|www\.\S+", "", text)
    # Remove punctuation
    text = text.translate(translator)
    # Remove extra spaces
    text = re.sub(r"\s+", " ", text).strip()
    # Tokenize
    tokens = safe_word_tokenize(text)
    # Remove stopwords
    tokens = [
        token
        for token in tokens
        if token not in stop_words or token in protected_words
    ]
    # Lemmatization
    tokens = [safe_lemmatize(token) for token in tokens]
    return " ".join(tokens)


# ---------------------------------
# Embedding Preprocessing
# ---------------------------------
def preprocess_for_embedding(text):
    if text is None:
        return ""
    text = str(text).lower()
    # Remove URLs only
    text = re.sub(r"http\S+|www\.\S+", "", text)
    # Normalize spaces
    text = re.sub(r"\s+", " ", text).strip()
    return text


# ---------------------------------
# Load documents from Excel
# ---------------------------------
# The Excel file is expected to sit next to this script.
_DATA_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "egyptian_greek_myths_filled.xlsx",
)


def load_documents(path: str = _DATA_PATH):
    """
    Reads the myths Excel file and returns a list of dicts shaped like:
        {
            "id": <str>,
            "title": <str>,
            "text": <str>,
            "is_current": <str/bool>,
        }
    """
    df = pd.read_excel(path, sheet_name="Myths")

    docs = []
    for _, row in df.iterrows():
        docs.append(
            {
                "id": str(row["ID"]),
                "title": str(row["Name"]),
                "text": str(row["Myth"]),
                "is_current": row["Historically Accurate?"],
                # Extra fields kept around in case they're useful later
                "civilization": row.get("Civilization"),
                "role": row.get("Role"),
            }
        )
    return docs


# Module-level `documents` used by chunking.py / embedding.py
documents = load_documents()


if __name__ == "__main__":
    print(f"Loaded {len(documents)} documents")
    print("-" * 80)
    print(documents[0])
    print("-" * 80)
    print(preprocess_for_bm25(documents[0]["text"][:200]))

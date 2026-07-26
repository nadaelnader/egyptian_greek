# -*- coding: utf-8 -*-
"""
Preprocessing module.

Loads the Egyptian/Greek myths dataset from Excel and provides
text-cleaning utilities used for BM25 and embedding-based retrieval.
"""

import re
import string

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

lemmatizer = WordNetLemmatizer()
translator = str.maketrans("", "", string.punctuation)

# Important words that should never be removed
protected_words = {
    "not", "no", "nor", "never",
    "egyptian", "greek",
    "god", "goddess",
    "pharaoh", "king",
    "queen", "myth",
    "historical", "history"
}

try:
    stop_words = set(stopwords.words("english"))
except LookupError:
    stop_words = {
        "the", "is", "and", "a", "an",
        "of", "to", "in", "for", "with",
        "on", "at", "by", "from"
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

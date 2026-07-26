# -*- coding: utf-8 -*-
"""
Preprocessing module.

Loads the Egyptian/Greek myths dataset from Excel and provides
text-cleaning utilities used for BM25 and embedding-based retrieval.
"""

import re
import string

translator = str.maketrans("", "", string.punctuation)


def preprocess_for_bm25(text):
    if text is None:
        return ""

    text = str(text).lower()
    text = text.translate(translator)
    text = re.sub(r"\s+", " ", text).strip()

    return text


def preprocess_for_embedding(text):
    if text is None:
        return ""

    text = str(text).lower()
    text = re.sub(r"http\S+|www\.\S+", "", text)
    text = re.sub(r"\s+", " ", text).strip()

    return text

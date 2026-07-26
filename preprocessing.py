# -*- coding: utf-8 -*-
"""
Preprocessing module.

Loads the Egyptian/Greek myths dataset from Excel and provides
text-cleaning utilities used for BM25 and embedding-based retrieval.
"""

import re
import string
import pandas as pd

FILE_PATH = "egyptian_greek_myths_filled.xlsx"

df = pd.read_excel(FILE_PATH)

documents = []

for _, row in df.iterrows():

    text = f"""
    Name: {row['Name']}
    Civilization: {row['Civilization']}
    Role: {row['Role']}
    Myth: {row['Myth']}
    Historically Accurate: {row['Historically Accurate?']}
    """

    documents.append(
        {
            "id": str(row["ID"]),
            "title": row["Name"],
            "is_current": True,
            "text": text.strip(),
        }
    )


def preprocess_for_bm25(text):

    if text is None:
        return ""

    text = str(text).lower()

    # remove punctuation
    text = text.translate(
        str.maketrans("", "", string.punctuation)
    )

    # remove extra spaces
    text = re.sub(r"\s+", " ", text).strip()

    return text

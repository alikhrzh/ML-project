import nltk
#!pip install transformers keybert pandas numpy scikit-learn
#nltk.download('wordnet')
#!pip install "sentence-transformers<3.0.0"

import re
import pandas as pd
import numpy as np
import torch

from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from keybert import KeyBERT
from nltk.corpus import wordnet
from sklearn.metrics.pairwise import cosine_similarity

class BulletproofTranslator:
    def __init__(self, model_name, device=0):
        self.device = f"cuda:{device}" if torch.cuda.is_available() else "cpu"
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name).to(self.device)

    def __call__(self, text, max_length=512):
        inputs = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=max_length).to(self.device)
        outputs = self.model.generate(**inputs, max_length=max_length)
        translated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

        return [{'translation_text': translated_text}]

translator = BulletproofTranslator("Helsinki-NLP/opus-mt-ru-en", device=0)

class SafeSentenceTransformer:
    def __init__(self, model_name):
        self.model = SentenceTransformer(model_name)

    def encode(self, texts, **kwargs):
        if isinstance(texts, np.ndarray):
            texts = texts.tolist()
        return self.model.encode(texts, **kwargs)

kw_model = KeyBERT(model=SafeSentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2'))

def normalize(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r'[^Ѐ-ӿÀ-ÿ\w\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text)

    if re.search(r'[\u0400-\u04FF]', text):
        text = translator(text, max_length=512)[0]['translation_text'].lower()

    return text.strip()

def expansion(text: str) -> str:
    if len(text.split()) > 6:
        return text

    keywords = kw_model.extract_keywords(text, keyphrase_ngram_range=(1,1), top_n=3)
    keywords = [kw for kw, score in keywords]

    additions = []
    for word in keywords:
        syns = wordnet.synsets(word)
        for syn in syns[:2]:
            for lemma in syn.lemmas()[:2]:
                name = lemma.name().replace('_', ' ')
                if name != word:
                    additions.append(name)

    return text + ' ' + ' '.join(additions) if additions else text

df = pd.read_csv('data/clubs_with_interest_areas.csv')

sent_model  = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

club_embeddings = np.load('data/club_embeddings.npy')

def get_sim_score(user_text: str) -> pd.DataFrame:
    text = normalize(user_text)
    text = expansion(text)

    # print(f"DEBUG: Processed input -> {text}")

    if not text.strip():
        return pd.DataFrame({
            'id': df['id'].values,
            'sim_score': np.zeros(len(df))
        })

    clean_text = str(text)

    query_vec = sent_model.encode([clean_text], convert_to_numpy=True)

    raw_scores = cosine_similarity(query_vec, club_embeddings)[0]

    scores = np.clip(raw_scores, 0, 1)

    return pd.DataFrame({
        'id': df['id'].values,
        'sim_score': scores
    }).sort_values('sim_score', ascending=False).reset_index(drop=True)

#print(get_sim_score("мне очень сильно нравится играть в футбол, хочу участвовать в соревнованиях по футбол"))
#print(get_sim_score("i want to became a data scientist and develop my CV and find new connectins"))
# df[df['id'] == 20]['name']
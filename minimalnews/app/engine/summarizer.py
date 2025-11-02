from heapq import nlargest
import string

import spacy
import en_core_web_sm
from spacy.lang.en.stop_words import STOP_WORDS


def summarize(text, by=30):
    """ Returns a summarized version of the text of the length 'by' % of the original text"""
    punctuation = string.punctuation
    punctuation += '\n'
    nlp = en_core_web_sm.load()
    doc = nlp(text)

    word_frequency = dict()
    for word in doc:
        if word.text.lower() not in STOP_WORDS:
            if word.text.lower() not in punctuation:
                word_frequency[word.text] = word_frequency.get(
                    word.text, 0) + 1

    max_frequency = max(word_frequency.values())

    # Normalization
    for word in word_frequency:
        word_frequency[word] /= max_frequency

    # Sentence tokenization
    sentence_tokens = [sentence for sentence in doc.sents]
    sentence_scores = dict()
    for sentence in sentence_tokens:
        for word in sentence:
            if word.text.lower() in word_frequency.keys():
                sentence_scores[sentence] = sentence_scores.get(
                    sentence, 0) + word_frequency[word.text.lower()]

    select_length = int(len(sentence_tokens) * (by / 100))
    summary = nlargest(select_length, sentence_scores, key=sentence_scores.get)
    formatted_summary = ' '.join([word.text for word in summary])

    return formatted_summary

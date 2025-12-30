import spacy
import nltk

class NLPTools:
    def __init__(self, model="en_core_web_sm"):
        try:
            self.nlp = spacy.load(model)
        except OSError:
            print(f"Model {model} not found. Please download it.")
            self.nlp = None

    def process_text(self, text):
        if self.nlp:
            return self.nlp(text)
        return text

    def get_entities(self, text, label=None):
        doc = self.process_text(text)
        if not isinstance(doc, spacy.tokens.Doc):
            return []
        
        entities = []
        for ent in doc.ents:
            if label:
                if ent.label_ == label:
                    entities.append(ent.text)
            else:
                entities.append((ent.text, ent.label_))
        return entities

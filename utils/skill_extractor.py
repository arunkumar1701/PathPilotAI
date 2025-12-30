from .nlp_tools import NLPTools

class SkillExtractor:
    def __init__(self):
        self.nlp_tools = NLPTools()
        # A simple predefined list or integration with a skills database would be better
        self.common_skills = {"python", "java", "sql", "machine learning", "data analysis", "react", "node.js"}

    def extract_skills(self, text):
        """
        Extract skills from text using simple matching and NER (ORG/PRODUCT usually capture some libs).
        """
        found_skills = set()
        text_lower = text.lower()
        
        # Simple string matching
        for skill in self.common_skills:
            if skill in text_lower:
                found_skills.add(skill)
        
        # NER based extraction (heuristic)
        entities = self.nlp_tools.get_entities(text)
        for ent, label in entities:
            if label in ["ORG", "PRODUCT", "WORK_OF_ART", "LANGUAGE"]:
                if ent.lower() not in found_skills:
                   # Potentially a skill, but needs filtering. 
                   # For now, just adding specific ones or relying on the common list is safer for a demo.
                   pass
        
        return list(found_skills)

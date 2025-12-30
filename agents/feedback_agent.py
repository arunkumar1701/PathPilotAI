class FeedbackAgent:
    def __init__(self, llm_manager=None):
        self.llm = llm_manager

    def analyze_feedback(self, text):
        if self.llm and self.llm.api_key:
             # In a real app, 'text' would be aggregate interview logs or work logs
             # For now we will just hallucinate meaningful feedback based on 'text' dummy
             return self._analyze_with_llm(text)
        return {
            "sentiment": "Positive",
            "key_areas": ["Confidence", "Technical Depth"],
            "score": 8.5
        }
        
    def _analyze_with_llm(self, text):
        prompt = f"""
        Analyze the following interview/feedback logs and generate constructive feedback.
        Logs: {text[:4000]}
        
        Return JSON with:
        - sentiment (string)
        - key_areas (list of strings, areas to improve)
        - score (float 1.0-10.0)
        """
        try:
            response = self.llm.get_response(prompt, structure_response=True)
            if isinstance(response, dict): return response
            return self._mock_feedback()
        except:
            return self._mock_feedback()

    def _mock_feedback(self):
        return {
            "sentiment": "Positive",
            "key_areas": ["System Design", "Cloud Native Patterns"],
            "score": 8.8
        }

    def analyze_rejection_patterns(self, rejection_texts):
        """
        Uses LDA to find common themes in rejection reasons.
        rejection_texts: list of strings (e.g., from emails)
        """
        from sklearn.feature_extraction.text import CountVectorizer
        from sklearn.decomposition import LatentDirichletAllocation
        import numpy as np

        if not rejection_texts or len(rejection_texts) < 3:
            return ["Not enough data for pattern analysis"]
        
        try:
            # Vectorize
            cv = CountVectorizer(max_df=0.95, min_df=2, stop_words='english')
            dtm = cv.fit_transform(rejection_texts)
            
            # LDA
            lda = LatentDirichletAllocation(n_components=3, random_state=42)
            lda.fit(dtm)
            
            # Extract topics
            topics = []
            feature_names = cv.get_feature_names_out()
            for index, topic in enumerate(lda.components_):
                # Getting top 3 words for each topic
                top_words = [feature_names[i] for i in topic.argsort()[-3:]]
                topics.append(f"Pattern {index+1}: {', '.join(top_words)}")
                
            return topics
        except Exception as e:
            return [f"Analysis failed: {str(e)}"]

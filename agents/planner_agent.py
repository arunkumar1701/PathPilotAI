class PlanningAgent:
    def __init__(self, llm_manager=None):
        self.llm = llm_manager

    def generate_roadmap(self, profile_data, market_data):
        if self.llm and self.llm.api_key:
            return self._generate_with_llm(profile_data, market_data)
        else:
            return self._mock_roadmap()

    def _generate_with_llm(self, profile_data, market_data):
        prompt = f"""
        Create a 4-week learning roadmap for a candidate with skills: {profile_data.get('skills')} 
        targeting the role: {market_data.get('role')}.
        The market demands these skills: {market_data.get('missing_skills')}.
        
        Return a JSON list of objects, where each object has:
        - week (integer)
        - focus (string title)
        - tasks (string with bullet points)
        - resources (list of objects with 'title' and 'url')
        """
        try:
            response = self.llm.get_response(prompt, structure_response=True)
            if isinstance(response, list):
                return response
            return self._mock_roadmap()
        except:
             return self._mock_roadmap()

    def _mock_roadmap(self):
        return [
            {
                "week": 1,
                "focus": "Core AI Foundations",
                "tasks": "- Complete 'Attention is All You Need' paper review\n- Build a simple RAG pipeline",
                "resources": [{"title": "LangChain Docs", "url": "https://python.langchain.com"}]
            },
            {
                "week": 2,
                "focus": "Advanced Engineering",
                "tasks": "- Dockerize application\n- Deploy to Hugging Face",
                "resources": []
            }
        ]

from utils.job_scraper import JobScraper
import random

class MarketAgent:
    def __init__(self, llm_manager=None):
        self.llm = llm_manager
        self.scraper = JobScraper()

    def forecast_demand(self, role, historical_data=None):
        """
        Predictive modeling using lightweight logic (Mocking Prophet/ARIMA for now).
        In a real scenario, this would fit a model to historical_data.
        """
        # Mock forecast
        return {
            "role": role,
            "next_quarter_demand": "+15%",
            "confidence_interval": "12% - 18%"
        }

    def analyze_market(self, role):
        if self.llm and self.llm.api_key:
            return self._analyze_with_llm(role)
        else:
            return self._mock_analysis(role)

    def _analyze_with_llm(self, role):
        prompt = f"""
        Act as a market research expert for potential candidates. Analyze the job market for the role: '{role}'.
        Return a JSON object with:
        - role (string)
        - growth_rate (string, e.g. "+20%")
        - salary_range (string)
        - competition (string: Low, Moderate, High)
        - missing_skills (list of 3 important advanced skills for this role)
        - skill_demand (dictionary where keys are skills and values are demand percentage 0-100. Must have 5 skills)
        - trending_keywords (list of 3 hot tech terms)
        """
        try:
            response = self.llm.get_response(prompt, structure_response=True)
            if isinstance(response, dict):
                return response
            return self._mock_analysis(role)
        except:
            return self._mock_analysis(role)

    def _mock_analysis(self, role):
        skills = {
            "Generative AI": 95,
            "MLOps": 80,
            "Python": 90,
            "Cloud Computing": 75,
            "HubSpot/Salesforce": 60
        }
        
        return {
            "role": role,
            "growth_rate": "+24% (Mock)",
            "salary_range": "$95k - $140k",
            "competition": "High",
            "missing_skills": ["MLOps", "Model Deployment", "Kubernetes"],
            "skill_demand": skills,
            "trending_keywords": ["Transformers", "LangChain", "RAG"]
        }

from utils.resume_parser import ResumeParser
import re

class ProfileAgent:
    def __init__(self, llm_manager=None):
        self.llm = llm_manager
        self.parser = ResumeParser()

    def parse_resume(self, file_obj):
        """
        Parses the uploaded PDF resume.
        file_obj: Stream/BytesIO from streamlit uploader
        """
        text = ""
        try:
            # Streamlit UploadedFile has .read() which returns bytes
             bytes_data = file_obj.read()
             text = self.parser.parse_pdf(bytes_data, is_stream=True)
             if not text:
                 text = "Error reading PDF or empty"
        except Exception as e:
            text = f"Error reading PDF: {e}"

        if self.llm and self.llm.api_key:
            return self._analyze_with_llm(text)
        else:
            return self._mock_analysis(text)

    def _analyze_with_llm(self, text):
        prompt = f"""
        Analyze the following resume text and return a JSON object with these exact keys:
        - name (string)
        - email (string)
        - education (list of strings)
        - skills (list of strings)
        - experience_level (string: Entry, Mid, Senior)
        - target_role (string: best fit role)
        - readiness_score (integer 0-100)
        
        Resume Text:
        {text[:2000]}
        """
        try:
            response = self.llm.get_response(prompt, structure_response=True)
            if isinstance(response, dict):
                response['raw_text'] = text
                if 'readiness_score' not in response: response['readiness_score'] = 50
                return response
            else:
                return self._mock_analysis(text) # Fallback if JSON parsing fails
        except:
            return self._mock_analysis(text)

    def _mock_analysis(self, text):
        return {
            "name": "Candidate (Demo)",
            "email": "demo@example.com",
            "education": ["B.Tech Computer Science (Detected)"],
            "skills": ["Python", "Streamlit", "Data Analysis", "React", "Node.js"] + ["Mock Skill 1", "Mock Skill 2"],
            "experience_level": "Entry-Level",
            "target_role": "AI Engineer",
            "readiness_score": 60,
            "raw_text": text[:500] + "..."
        }

import speech_recognition as sr

class ActionAgent:
    def __init__(self, llm_manager=None):
        self.llm = llm_manager
        self.recognizer = sr.Recognizer()
        # Define a structured pool of questions for mock mode
        self.question_pool = [
            "Could you introduce yourself and briefly explain your background in AI?",
            "Can you elaborate on your experience with Python, specifically with libraries like Pandas or PyTorch?",
            "Tell me about a challenging project you've worked on. What was the core technical hurdle?",
            "How do you handle a conflict within your team? Give me a specific example.",
            "What metrics would you prioritize when evaluating a binary classification model?",
            "Describe a time you had to optimize a slow-running pipeline or query.",
            "How do you stay updated with the latest in Generative AI and LLMs?",
            "That covers the basics. do you have any questions for me regarding the role?"
        ]

    def transcribe_audio(self, audio_data):
        """
        Transcribes audio data to text using Google Speech Recognition.
        audio_data: Audio data from source (file or microphone)
        """
        try:
            # Assuming audio_data is a file path or AudioSource. 
            # If it's a file path:
            if isinstance(audio_data, str):
                with sr.AudioFile(audio_data) as source:
                    audio = self.recognizer.record(source)
                return self.recognizer.recognize_google(audio)
            else:
                 # If it's distinct audio bytes, might need different handling
                 return "Transcribed text (Mock): Audio processing requires active microphone."
        except sr.RequestError:
            return "API unavailable"
        except sr.UnknownValueError:
            return "Unable to recognize speech"
        except Exception as e:
            return f"Error: {e}"

    def auto_apply(self, job_dict):
        """
        Simulates applying to a job.
        """
        # In a real app, this would use Selenium/Playwright or an API
        return {
            "success": True, 
            "message": f"Application submitted to {job_dict.get('company')} for {job_dict.get('title')}"
        }

    def get_matched_jobs(self, profile_data, market_data):
        """
        Returns a list of jobs matched to the user profile.
        """
        # Mock jobs or filtered from JobScraper
        target_role = profile_data.get('target_role', 'Engineer')
        
        # Simple Mock DB
        jobs = [
            {"id": 1, "title": f"Senior {target_role}", "company": "TechCorp", "match_score": 95, "location": "Remote"},
            {"id": 2, "title": f"{target_role}", "company": "DataLabs", "match_score": 88, "location": "San Francisco"},
            {"id": 3, "title": "AI Research Scientist", "company": "OpenMind", "match_score": 75, "location": "London"},
            {"id": 4, "title": "Machine Learning Engineer", "company": "InnovateAI", "match_score": 92, "location": "Remote"}
        ]
        
        # Filter logic can go here
        return jobs

    def conduct_interview(self, history, user_input, context=""):
        """
        Conducts an interview turn using the LLM.
        """
        if self.llm and self.llm.api_key:
            return self.llm.chat_response(history, user_input, context=context)
        else:
            return self._mock_interview_smart(history, user_input)

    def _mock_interview_smart(self, history, user_input):
        import random
        
        # 1. Analyze what has already been asked
        asked_questions = set()
        for msg in history:
            if msg['role'] == 'assistant':
                asked_questions.add(msg['content'])

        # 2. Simple Context Awareness (Keyword-based)
        lower_input = user_input.lower()
        
        # If user gives a very short answer
        if len(user_input.split()) < 3 and "hi" not in lower_input and "hello" not in lower_input:
            return "Could you elaborate a bit more on that? I'd love to hear specific details."

        # If user talks about a project, ask about tech stack
        if "project" in lower_input or "built" in lower_input or "system" in lower_input:
            return "That sounds like an impactful project. What specific technology stack did you choose for it, and why?"

        # If user talks about conflict, ask about outcome
        if "conflict" in lower_input or "disagreement" in lower_input:
            return "Communication is key. What was the final outcome of that situation? Did the team align?"

        # 3. Pick the next logical question that hasn't been asked
        for question in self.question_pool:
            if question not in asked_questions:
                return question
        
        # Fallback if all questions asked
        return "Thank you for sharing all that. We've covered a lot of ground. I'll review your responses and get back to you shortly!"

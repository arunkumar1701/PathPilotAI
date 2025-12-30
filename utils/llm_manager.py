import google.generativeai as genai
import json
import streamlit as st

class LLMManager:
    def __init__(self, api_key=None):
        self.api_key = api_key
        if self.api_key:
            genai.configure(api_key=self.api_key)
            try:
                # Dynamic model selection
                available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                priority_models = ['models/gemini-1.5-flash', 'models/gemini-pro', 'models/gemini-1.0-pro']
                
                selected_model = None
                # Try priority first
                for p in priority_models:
                    if p in available_models:
                        selected_model = p
                        break
                
                # Fallback to first available
                if not selected_model and available_models:
                    selected_model = available_models[0]
                
                if selected_model:
                    self.model = genai.GenerativeModel(selected_model)
                else:
                    self.model = genai.GenerativeModel('gemini-pro') # Last resort
            except Exception as e:
                print(f"Error selecting model: {e}")
                self.model = genai.GenerativeModel('gemini-pro')
        
    def get_response(self, prompt, structure_response=False):
        if not self.api_key:
            return "⚠️ API Key missing. Please provide a Google Gemini API Key in the sidebar."
        
        try:
            response = self.model.generate_content(prompt)
            content = response.text
            
            if structure_response:
                # Attempt to clean and parse JSON
                content = content.replace('```json', '').replace('```', '').strip()
                try:
                    return json.loads(content)
                except json.JSONDecodeError:
                    return content # Fallback if not valid JSON
            return content
        except Exception as e:
            return f"Error interacting with AI: {str(e)}"

    def chat_response(self, history, user_input, context=""):
        if not self.api_key:
            return "⚠️ API Key missing."

        # Construct prompt from history for context-aware chat
        # Gemini Pro supports chat history object, but manual prompting is often more robust for specific personas
        
        system_prompt = f"""
        You are an expert technical interviewer for AI/ML roles. 
        Context: {context}
        Current Interview State: {history}
        User just said: {user_input}
        
        Task:
        1. Analyze the user's answer.
        2. If the answer is weak or "I don't know", ask a simpler follow-up or explain the concept briefly then move on.
        3. If the answer is good, dig deeper.
        4. Keep responses concise and conversational. Do NOT repeat questions.
        5. If the user asks for feedback, give it.
        6. Address them by name if known.
        """
        
        try:
            response = self.model.generate_content(system_prompt)
            return response.text
        except Exception as e:
            return f"Error: {str(e)}"

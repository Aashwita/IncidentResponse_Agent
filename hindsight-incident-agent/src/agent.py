from groq import Groq
from src.config import GROQ_API_KEY
from src.memory import HindsightMemoryClient

class IncidentAgent:
    def __init__(self):
        self.groq_client = Groq(api_key=GROQ_API_KEY)
        self.memory = HindsightMemoryClient()
        self.model = "qwen/qwen3-32b" 

    def analyze_incident(self, error_log: str) -> str:
        past_memories = self.memory.recall_memory(query=error_log, limit=2)
        context_str = "\n".join([f"- {m.get('content', '')}" for m in past_memories]) if past_memories else "No direct historical matches found."

        system_prompt = (
            "You are an expert Autonomous Incident Response Agent with persistent memory. "
            "Your job is to diagnose production errors, suggest root causes, and provide step-by-step remediation plans. "
            "Use the provided historical memory from past incidents to make your recommendation accurate and tailored to this environment."
        )

        user_prompt = (
            f"Incoming Error Log:\n{error_log}\n\n"
            f"Relevant Historical Memory (from Hindsight):\n{context_str}\n\n"
            "Provide a concise diagnosis and a step-by-step resolution plan based on the above."
        )

        try:
            chat_completion = self.groq_client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.2,
                max_tokens=1024
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            return f"Error during LLM generation: {str(e)}"
import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class LeadQualifier:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def qualify_lead(self, inquiry_text):
        """
        Parses lead data and returns a qualification score and next steps.
        """
        system_instructions = (
            "You are a Lead Qualification Specialist. Analyze inquiries and return "
            "a JSON object with keys: 'score' (1-10), 'is_qualified' (bool), and 'reason'."
        )

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_instructions},
                    {"role": "user", "content": inquiry_text}
                ],
                response_format={ "type": "json_object" }
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            return {"error": str(e)}

if __name__ == "__main__":
    qualifier = LeadQualifier()
    
    # Simulate a hot lead
    hot_lead = "Hi Kenneth, I'm looking for a full CRM automation for my real estate firm. My budget is $5,000."
    
    result = qualifier.qualify_lead(hot_lead)
    print(f"Lead Score: {result.get('score')}/10")
    print(f"Action: {'Schedule Call' if result.get('is_qualified') else 'Send Rejection'}")

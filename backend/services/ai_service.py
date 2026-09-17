import openai
import json
from typing import Dict, Any, List
from ..config import settings

def _get_client():
    return openai.OpenAI(api_key=settings.OPENAI_API_KEY)

def classify_complaint(subject: str, description: str, category_hint: str = None) -> Dict[str, Any]:
    default_response = {
        "category": "General",
        "subcategory": "Other",
        "priority": "medium",
        "sentiment": "neutral",
        "urgency": "low",
        "department_suggestion": "Customer Relations",
        "escalation_flag": False
    }
    
    if not settings.OPENAI_API_KEY:
        return default_response

    prompt = f\"\"\"Classify the following customer complaint:
Subject: {subject}
Description: {description}
Hint: {category_hint or 'None'}

Return a JSON object with the following keys:
- category (string)
- subcategory (string)
- priority (low/medium/high/critical)
- sentiment (positive/neutral/negative/angry)
- urgency (low/medium/high)
- department_suggestion (string)
- escalation_flag (boolean)
\"\"\"
    try:
        client = _get_client()
        response = client.chat.completions.create(
            model=settings.CHAT_MODEL,
            messages=[
                {"role": "system", "content": "You are a customer service AI assistant. Respond ONLY with valid JSON."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        print(f"Classification error: {e}")
        return default_response

def generate_response(complaint_data: Dict[str, Any], context: str, tone: str, channel: str) -> str:
    if not settings.OPENAI_API_KEY:
        return f"Mock response for complaint {complaint_data.get('reference_number')} via {channel} with {tone} tone."
        
    prompt = f\"\"\"Generate a response for this complaint:
Complaint: {json.dumps(complaint_data, default=str)}
Relevant Knowledge Base Context: {context}

Requirements:
- Tone: {tone}
- Channel: {channel}
- Be empathetic and professional.
- Propose a resolution if context allows.
\"\"\"
    try:
        client = _get_client()
        response = client.chat.completions.create(
            model=settings.CHAT_MODEL,
            messages=[
                {"role": "system", "content": "You are a helpful customer service AI assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Generation error: {e}")
        return "Failed to generate AI response."

def generate_business_insights(analytics_data: Dict[str, Any]) -> str:
    if not settings.OPENAI_API_KEY:
        return "Insight generation requires OpenAI API Key."
        
    prompt = f"Analyze this complaint data and provide 3 key business insights:\n{json.dumps(analytics_data)}"
    try:
        client = _get_client()
        response = client.chat.completions.create(
            model=settings.CHAT_MODEL,
            messages=[
                {"role": "system", "content": "You are a business intelligence analyst."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Insights error: {e}")
        return "Failed to generate insights."

def detect_escalation_triggers(complaint_data: Dict[str, Any]) -> Dict[str, Any]:
    if not settings.OPENAI_API_KEY:
        return {"should_escalate": False, "reason": ""}
        
    prompt = f\"\"\"Analyze if this complaint should be escalated to management:
{json.dumps(complaint_data, default=str)}

Return JSON with keys: 'should_escalate' (bool), 'reason' (string)
\"\"\"
    try:
        client = _get_client()
        response = client.chat.completions.create(
            model=settings.CHAT_MODEL,
            messages=[
                {"role": "system", "content": "You are an escalation manager. Respond with JSON."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)
    except Exception:
        return {"should_escalate": False, "reason": "Error detecting"}

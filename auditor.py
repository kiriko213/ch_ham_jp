import os
import google.generativeai as genai
import re
import json

def audit_dog_content(title, content, keyword, api_key=None):
    """
    AI監査員 (Hamster Paradise Version)
    投稿内容が「ハムスター」に特化しているか、他の動物が混じっていないかを厳格にチェックします。
    """
    if api_key:
        genai.configure(api_key=api_key)
    
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    audit_prompt = f"""
    You are a HIGHLY STRICT Content Compliance Officer for the YouTube channel "Hamster Paradise (ハムスターの楽園)".
    
    Current Content to Audit:
    Title: {title}
    Content: {content}
    Search Keyword: {keyword}
    
    === QUALITY & SAFETY RULES ===
    1. NO OTHER ANIMALS: This channel is EXCLUSIVELY for hamsters. Absolute FAIL if cats, dogs, or any other animals are mentioned or suggested.
    2. NO EMOJIS OR SYMBOLS: Use ONLY letters and basic punctuation. FAIL if you see any.
    3. SHORT & PUNCHY: Must be readable within 15 seconds.
    
    === OUTPUT FORMAT ===
    Result: [PASS or FAIL]
    Feedback: [If FAIL, explain why. Mention if a forbidden animal was found.]
    """
    
    try:
        response = model.generate_content(audit_prompt)
        text = response.text
        
        is_pass = "Result: PASS" in text
        feedback = ""
        if "Feedback:" in text:
            match = re.search(r"Feedback:\s*(.*)", text, re.DOTALL)
            if match: feedback = match.group(1).strip()
            
        return is_pass, feedback
        
    except Exception as e:
        print(f"Audit Error: {e}")
        return False, "Audit system error."

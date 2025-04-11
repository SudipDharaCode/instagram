from fastapi import FastAPI, Request
from pydantic import BaseModel
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
import uvicorn




# ---------------------------
# LangChain Setup
# ---------------------------



chat = ChatGroq(temperature=0, groq_api_key="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", model_name="llama-3.3-70b-versatile")


system_prompt = """
You are an AI that analyzes social media comments and determines if they have commercial intent.
The comment can be from **Instagram, Facebook, YouTube, Twitter, or any platform** and can be about **any product or service**.

### **What is Commercial Intent?**
A comment has commercial intent if it shows interest in **buying, ordering, pricing, availability, delivery, or discounts**.

### **Special Instructions:**
- If the comment is empty("") or only contains symbols (like a single question mark, emoji, etc.), return **False**.
- Do not assume commercial intent unless there's a clear indication of interest in a product or service.

### Rules for Detection:
1. The comment **must clearly express** interest in a product or service.
2. If the comment is empty, or only contains punctuation or meaningless characters (e.g., `?`, `...`, `!`,"", emojis, or just whitespace), or only space or any text is writen , it does **not** have commercial intent.
3. If the comment is only space or nothing is writen .  it does **not** have commercial intent return **False**.
4. Do **not** assume commercial intent unless it is very clear from the comment.
5. Ignore generic compliments, greetings, or unrelated chatter.

User text : {text}

Example of Output :

[
  "Type": "True"  # If text is related to content creation
]

or

[
  "Type": "False"  # If text is NOT related to content creation
]
"""

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt)
])
chain = prompt | chat





# ---------------------------
# FastAPI Setup
# ---------------------------



app = FastAPI()

class CommentInput(BaseModel):
    text: str

@app.post("/analyze")
async def analyze_comment(data: CommentInput):
    try:
        if not data.text: return {"commercial_intent": false}
        output = chain.invoke({"text": data.text})
        result = output.content.split('"Type": "')[1].split('"')[0]
        return {"commercial_intent": result}
    except Exception as e:
        return {"error": str(e)}

# ---------------------------
# Run with: uvicorn filename:app --reload
# ---------------------------
if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True) 


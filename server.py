import uvicorn
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai

# 1. Setup the Brain (Gemini)
# We use os.getenv to pull the key SECURELY from Railway Variables
api_key = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=AIzaSyARIrVwmX5H906TluwCrqbtrkc5J1VfiG4)

app = FastAPI()

# 2. Setup the Bridge (CORS) 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    print(f"User asked: {request.message}")
    
    # Check if API Key exists
    if not api_key:
        return {"reply": "Backend Error: GOOGLE_API_KEY is not set in Railway variables."}
    
    try:
        # 3. Generating the response from Gemini
        response = client.models.generate_content(
            model="gemini-1.5-flash", # Updated to a more standard model name
            config={
                'system_instruction': "You are Finwise AI, a bilingual financial mentor for Pakistan. Speak in Roman Urdu and English. Be professional yet friendly. Always add a small legal disclaimer at the end."
            },
            contents=request.message
        )
        
        return {"reply": response.text}
        
    except Exception as e:
        print(f"Error: {e}")
        return {"reply": "Maazrat, connectivity ka masla hai. Please check your Railway logs."}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)

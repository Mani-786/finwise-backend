import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai

# 1. Setup the Brain (Gemini)
# REPLACE 'YOUR_API_KEY' with the key you got from Google AI Studio
client = genai.Client(api_key="AIzaSyBw41Xpm7wU4Ggm8ZXDgWaqU8MKF7qel_I")

app = FastAPI()

# 2. Setup the Bridge (CORS) 
# This tells your computer to allow the Bolt website to talk to this script
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
    
    try:
        # 3. Generating the response from Gemini
        response = client.models.generate_content(
            model="gemini-flash-lite-latest",
            config={
                'system_instruction': "You are Finwise AI, a bilingual financial mentor for Pakistan. Speak in Roman Urdu and English. Be professional yet friendly. Always add a small legal disclaimer at the end."
            },
            contents=request.message
        )
        
        # 4. Sending it back to the UI in the format it expects
        return {"reply": response.text}
        
    except Exception as e:
        print(f"Error: {e}")
        return {"reply": "Maazrat, connectivity ka masla hai. Please check your terminal."}

import os
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

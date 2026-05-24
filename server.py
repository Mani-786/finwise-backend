import os
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from google import genai
from pydantic import BaseModel

# Initialize FastAPI app
app = FastAPI()

# Enable CORS for your Netlify frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can replace "*" with your specific Netlify URL later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat_endpoint(chat_request: ChatRequest):
    # Retrieve the API Key inside the function to ensure Railway has loaded it
    api_key = os.environ.get("GOOGLE_API_KEY")
    
    if not api_key:
        print("ERROR: GOOGLE_API_KEY environment variable is missing!")
        raise HTTPException(status_code=500, detail="Server configuration error: Missing API Key")

    try:
        # Initialize the Gemini client locally within the request
        client = genai.Client(api_key=api_key)
        
        # Call the Gemini API
        response = client.models.generate_content(
            model="gemini-1.5-flash", 
            contents=chat_request.message
        )
        
        return {"reply": response.text}

    except Exception as e:
        print(f"Error during API call: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"status": "Finwise Backend is running"}

if __name__ == "__main__":
    import uvicorn
    # Railway provides the PORT environment variable automatically
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)

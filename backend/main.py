from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import yt_dlp
from openai import OpenAI
import os
from dotenv import load_dotenv

app = FastAPI()

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# print("OPENAI_API_KEY", OPENAI_API_KEY)
client = OpenAI()


# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class VideoRequest(BaseModel):
    url: str

def get_video_transcript(url: str) -> str:
    try:
        # Download audio from YouTube video
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': 'temp_audio',
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            
        # Use Whisper to transcribe the audio
        audio_path = "temp_audio.mp3"
        
        with open(audio_path, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )
            
        # Clean up temporary audio file
        os.remove(audio_path)
        
        return transcript.text
        
    except Exception as e:
        if os.path.exists("temp_audio.mp3"):
            os.remove("temp_audio.mp3")
        raise HTTPException(status_code=400, detail=f"Error getting transcript: {str(e)}")

def summarize_with_openai(transcript: str) -> str:
    try:
        context = "Please provide a comprehensive summary of this video transcript."
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes video transcripts."},
                {"role": "user", "content": f"{context}\n\nTranscript:\n{transcript}"}
            ],
            max_tokens=1000
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in summarization: {str(e)}")


def get_test_summary():
    with open("test_summary.txt", "r") as f:
        return f.read()


@app.post("/api/summarize")
async def summarize_video(request: VideoRequest):
    if request.url == "test":
        return {"summary": get_test_summary()}
    
    transcript = get_video_transcript(request.url)
    summary = summarize_with_openai(transcript)
    return {"summary": summary} 
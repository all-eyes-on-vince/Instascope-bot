from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from modules import spotify_integration, pinterest_integration, instagram_integration
from modules import mood_detector, lyrics_generator, zodiac_insights
from modules import caption_generator, scheduler, analytics, video_editor

app = FastAPI(
    title="Instascope API",
    description="Instascope: A powerful Instagram bot for music, art, mood detection, zodiac insights, and more.",
    version="1.0.0"
)

# Allow frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Welcome to Instascope 🚀"}

# ------------------------------
# Example API Routes
# ------------------------------

@app.get("/spotify/search")
def search_spotify(track: str):
    """Search for a track on Spotify"""
    return spotify_integration.search_track(track)

@app.post("/mood-detect")
async def mood_detect(file: UploadFile = File(...)):
    """Detect mood from uploaded photo"""
    contents = await file.read()
    return mood_detector.detect_mood(contents)

@app.get("/zodiac/{month}")
def zodiac(month: str):
    """Return zodiac insights based on birth month"""
    return zodiac_insights.get_zodiac(month)

@app.get("/pinterest/art")
def get_art(query: str = "fine art"):
    """Fetch art from Pinterest"""
    return pinterest_integration.fetch_art(query)

@app.post("/lyrics")
def generate_lyrics(song: str):
    """Generate lyrics for a given song title"""
    return lyrics_generator.generate(song)

@app.post("/caption")
def generate_caption(prompt: str):
    """Generate creative captions"""
    return caption_generator.generate(prompt)

@app.get("/analytics")
def get_analytics():
    """Return dummy analytics for now"""
    return analytics.get_stats()

@app.post("/schedule")
def schedule_post(time: str, content: str):
    """Schedule a post"""
    return scheduler.add_schedule(time, content)

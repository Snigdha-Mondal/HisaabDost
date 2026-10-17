import os
from pathlib import Path
from pydantic import BaseModel
from dotenv import load_dotenv

# Load .env if present
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseModel):
    # App info
    PROJECT_NAME: str = "HisaabDost"
    VERSION: str = "0.1.0"
    DEBUG: bool = os.getenv("DEBUG", "true").lower() in ("true", "1", "yes")
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))

    # File paths
    DATA_DIR: Path = BASE_DIR / "data"
    SAMPLE_HISTORY_PATH: Path = BASE_DIR / "data" / "sample_history.csv"
    SAMPLE_TRANSCRIPTS_PATH: Path = BASE_DIR / "data" / "sample_audio_transcripts.json"

    # Gemma 2 / AI settings
    GEMMA_API_KEY: str = os.getenv("GEMMA_API_KEY", "")
    GEMMA_MODEL_NAME: str = os.getenv("GEMMA_MODEL_NAME", "gemma-2-9b-it")
    USE_LOCAL_GEMMA: bool = os.getenv("USE_LOCAL_GEMMA", "false").lower() in ("true", "1")

    # TabPFN settings
    TABPFN_API_KEY: str = os.getenv("TABPFN_API_KEY", "")
    TABPFN_ANOMALY_THRESHOLD_PCT: float = float(os.getenv("TABPFN_ANOMALY_THRESHOLD_PCT", "8.0"))

    # ElevenLabs settings
    ELEVENLABS_API_KEY: str = os.getenv("ELEVENLABS_API_KEY", "")
    ELEVENLABS_VOICE_ID: str = os.getenv("ELEVENLABS_VOICE_ID", "pNInz6obpgDQGcFmaJgB")

    # Temporal settings
    TEMPORAL_HOST_URL: str = os.getenv("TEMPORAL_HOST_URL", "localhost:7233")
    TEMPORAL_TASK_QUEUE: str = os.getenv("TEMPORAL_TASK_QUEUE", "hisaabdost-voice-queue")

    # Twilio settings
    TWILIO_ACCOUNT_SID: str = os.getenv("TWILIO_ACCOUNT_SID", "")
    TWILIO_AUTH_TOKEN: str = os.getenv("TWILIO_AUTH_TOKEN", "")
    TWILIO_PHONE_NUMBER: str = os.getenv("TWILIO_PHONE_NUMBER", "+1234567890")

    # Sentry DSN
    SENTRY_DSN: str = os.getenv("SENTRY_DSN", "")

settings = Settings()

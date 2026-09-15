import whisper
import os

WHISPER_MODEL = os.getenv("WHISPER_MODEL", "turbo")

_model = None

def load_model():
    global _model
    if _model is None:
        print(f"loading model ...")
        _model = whisper.load_model(WHISPER_MODEL)
        print(f"whisper model loaded succesfully")
    return _model


def transcribe_chunk(chunk_path: str) -> dict:
    model = load_model()

    # Pehlay language detect karo (translate na karte hue)
    result = model.transcribe(chunk_path, task="transcribe")
    detected_lang = result["language"]

    # Agar English nahi hai, to translate karo
    if detected_lang != "en":
        result = model.transcribe(chunk_path, task="translate")

    return {
        "text": result["text"],
        "detected_language": detected_lang,
    }

def transcribe_all(chunks: list) -> str:
    full_transcript = ""
    for i, chunk in enumerate(chunks):
        print(f"Transcribing chunk {i + 1}/{len(chunks)}...")
        result = transcribe_chunk(chunk)
        full_transcript += result["text"] + " "
    print("Transcription complete.")
    return full_transcript.strip()
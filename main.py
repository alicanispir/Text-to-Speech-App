import fitz
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "YOUR-GOOGLE-CLOUD-KEY.json"

from google.cloud import texttospeech

client = texttospeech.TextToSpeechClient()
print("Google Cloud Text-to-Speech API is working correctly!")

def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF file."""
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text("text") + "\n"
    return text

def text_to_speech(text, output_audio="output.mp3"):
    client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)

    with open(output_audio, "wb") as out:
        out.write(response.audio_content)
        print(f"Audio content saved to {output_audio}")


if __name__ == "__main__":
    pdf_path = "random.pdf"  # Add your pdf file to the project folder
    extracted_text = extract_text_from_pdf(pdf_path)

    if extracted_text.strip():
        print("Extracted text:", extracted_text)
        text_to_speech(extracted_text)
    else:
        print("No text found in the PDF!")

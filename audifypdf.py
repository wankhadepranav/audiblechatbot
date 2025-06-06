import gradio as gr
from PyPDF2 import PdfReader
from gtts import gTTS
import os
import tempfile

def convert_pdf_to_audio_with_subtitles(pdf_file, voice_option, language):
    try:
        # Read the PDF
        reader = PdfReader(pdf_file)
        text = ""
        subtitles = []
        for page_num, page in enumerate(reader.pages, start=1):
            page_text = page.extract_text()
            if page_text:
                text += page_text
                subtitles.append(f"Page {page_num}: {page_text.strip()}")

        if not text.strip():
            return "No text found in PDF.", None, None

        # Generate audio with selected voice and language
        tts = gTTS(text, lang=language, tld=voice_option)
        temp_dir = tempfile.gettempdir()
        output_file = os.path.join(temp_dir, "audify_output.mp3")
        tts.save(output_file)

        # Combine subtitles into a single string
        subtitles_text = "\n\n".join(subtitles)

        return "✅ Audio generated successfully!", output_file, subtitles_text
    except Exception as e:
        return f"❌ Error: {str(e)}", None, None

# Define the Gradio interface
interface = gr.Interface(
    fn=convert_pdf_to_audio_with_subtitles,
    inputs=[
        gr.File(label="📄 Upload your PDF"),
        gr.Radio(
            choices=["com", "co.uk", "ca", "in"],
            label="🌍 Select Voice Accent",
            value="com",
            info="Choose the voice accent for the audio (e.g., US, UK, Canada, India)."
        ),
        gr.Dropdown(
            choices=["en", "es", "fr", "de", "hi", "mr"],
            label="🌐 Select Language",
            value="en",
            info="Choose the language for text-to-speech conversion (e.g., English, Spanish, French, Hindi, Marathi)."
        )
    ],
    outputs=[
        gr.Textbox(label="Status"),
        gr.Audio(label="🎧 Listen to the Audio"),
        gr.Textbox(label="📜 Subtitles (Extracted Text)")
    ],
    title="AudifyPDF with Subtitles and Multilingual Support",
    description="📘 Convert your PDF to spoken audio with subtitles, multiple voice accents, and multilingual support, including Marathi.",
    theme="default"
)

interface.launch()
import streamlit as st
from dotenv import load_dotenv
import os
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi

# Load environment variables
load_dotenv()

# Configure Google GenAI
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Prompt templates
summary_prompt = """You are a YouTube video summarizer. You will take the transcript text
and summarize the entire video, providing important points in 250 words. Please summarize the text given here: """

translation_prompt = """You are a professional translator. Translate the given text to {language}.
Provide a clear and accurate translation. Here is the text: """

qa_prompt = """You are a helpful assistant. Answer the following question based on the YouTube video transcript:
Transcript: {transcript}
Question: {question}
Answer: """

# Function to extract transcript details
def extract_transcript_details(youtube_video_url):
    try:
        video_id = youtube_video_url.split("=")[1]
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)

        transcript = ""
        for i in transcript_text:
            transcript += " " + i["text"]

        return transcript
    except Exception as e:
        raise e

# Function to generate summary using Gemini Pro
def generate_gemini_content(transcript_text, prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt + transcript_text)
    return response.text

# Function to translate text using GenAI
def translate_using_genai(text, language):
    translation_model = genai.GenerativeModel("gemini-pro")
    translation_response = translation_model.generate_content(
        translation_prompt.format(language=language) + text
    )
    return translation_response.text

# Function to handle Q&A using GenAI
def generate_qa_response(transcript_text, question):
    model = genai.GenerativeModel("gemini-pro")
    qa_response = model.generate_content(
        qa_prompt.format(transcript=transcript_text, question=question)
    )
    return qa_response.text

# Streamlit app UI
st.title("YouTube Video Summarizer and Q&A")

youtube_link = st.text_input("Enter YouTube Video Link:")

if youtube_link:
    video_id = youtube_link.split("=")[1]
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_container_width=True)

if st.button("Get Summary"):
    transcript_text = extract_transcript_details(youtube_link)
    summary = generate_gemini_content(transcript_text, summary_prompt)
    st.session_state["summary"] = summary  # Store summary in session state
    st.session_state["transcript"] = transcript_text  # Store transcript for Q&A
    st.markdown("## Summary:")
    st.write(summary)

if "summary" in st.session_state:
    summary = st.session_state["summary"]

    # Translation Section
    languages = {
        "Hindi": "Hindi",
        "Tamil": "Tamil",
        "Telugu": "Telugu",
        "Bengali": "Bengali",
        "Marathi": "Marathi",
        "Gujarati": "Gujarati",
        "Kannada": "Kannada",
        "Malayalam": "Malayalam",
        "Punjabi": "Punjabi",
        "Spanish": "Spanish",
        "French": "French"
    }

    selected_language = st.selectbox("Translate summary to:", options=list(languages.keys()))

    if st.button("Translate Summary"):
        translated_summary = translate_using_genai(summary, languages[selected_language])
        st.markdown(f"## Translated Summary in {selected_language}:")
        st.write(translated_summary)

    # Q&A Section
    st.markdown("## Ask a Question about the Video")
    question = st.text_input("Enter your question:")
    
    if st.button("Get Answer"):
        if question.strip():
            transcript_text = st.session_state["transcript"]
            answer = generate_qa_response(transcript_text, question)
            st.markdown("### Answer:")
            st.write(answer)
        else:
            st.error("Please enter a question.")

import os
import boto3
import json
import streamlit as st
from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter

# Use Amazon Bedrock
bedrock = boto3.client(
    service_name='bedrock-runtime',
    region_name='us-west-2'
)

# Ensure necessary directory exists
os.makedirs('transcripts', exist_ok=True)

def append_summary_to_file(summary, title, url):
    with open("summaries.txt", "a", encoding="utf-8") as file:
        file.write(f"Title: {title}\nURL: {url}\nSummary: {summary}\n\n")

def check_and_download_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        formatter = TextFormatter()
        transcript_text = formatter.format_transcript(transcript)
        with open(f'transcripts/{video_id}.txt', 'w', encoding='utf-8') as file:
            file.write(transcript_text)
        st.success("Transcript downloaded successfully.")
        return transcript_text
    except Exception as e:
        st.warning("No transcript available or an error occurred.")
        return None

def summarize_content(content):
    try:
        body = json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "messages": [
                {"role": "user", "content": f"Please summarize the following YouTube video transcript: {content}"}
            ],
            "max_tokens": 300,
            "temperature": 0.1,
            "top_p": 0.9,
            "system": "You are a YouTube video summarizer created for the purpose of writing show notes. Provide a summary that includes all the main points of the video. Mention any links and external resources shared in the video and encourage the reader to check out the video."
        })
        modelId = 'anthropic.claude-3-5-sonnet-20240620-v1:0'
        response = bedrock.invoke_model(body=body, modelId=modelId, accept='application/json', contentType='application/json')
        
        response_body = json.loads(response.get('body').read())
        
        if 'content' in response_body and isinstance(response_body['content'], list):
            for item in response_body['content']:
                if item['type'] == 'text':
                    return item['text'].strip()
        
        st.error("Unexpected response structure from Amazon Bedrock API")
        return None
    except Exception as e:
        st.error(f"An error occurred with the Amazon Bedrock API: {str(e)}")
        return None

def show_notes_generator():
    st.title("YouTube Show Notes Generator")
    video_url = st.text_input("Enter the YouTube video URL")

    if st.button("Generate Show Notes"):
        if video_url:
            video_id = YouTube(video_url).video_id
            yt = YouTube(video_url)
            try:
                transcript_text = check_and_download_transcript(video_id)
                if transcript_text:
                    st.text_area("Transcript", transcript_text, height=300)
                    summary = summarize_content(transcript_text)
                    if summary:
                        formatted_text = f"- [{yt.title}]({video_url}) - {summary}"
                        st.markdown(formatted_text, unsafe_allow_html=True)
                        copy_text = f"- {yt.title} ({video_url}) - {summary}"
                        st.text_area("Copy the show notes below:", copy_text, height=100)
                        append_summary_to_file(summary, yt.title, video_url)
                else:
                    st.warning("No transcript is available for this video.")
            except Exception as e:
                st.error(f"An error occurred: {e}")
        else:
            st.warning("Please enter a YouTube URL.")

# Main app
show_notes_generator()

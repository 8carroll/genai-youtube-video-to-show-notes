import os
import re
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI client with API key
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Ensure the 'videos' and 'transcripts' directories exist
os.makedirs('videos', exist_ok=True)
os.makedirs('transcripts', exist_ok=True)

def predict_category(summary):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "Categorize the summary as either a Technical Topic, Career Advice, or Certification and Learning."}, {"role": "user", "content": summary}]
        )
        category_prediction = response.choices[0].message.content.strip()
        return category_prediction
    except Exception as e:
        st.error(f"An error occurred while predicting the category: {e}")
        return "Unknown"

def identify_aws_services(text):
    try:
        prompt = "Identify all AWS services mentioned in the text: " + text
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": prompt}]
        )
        services_list = response.choices[0].message.content.strip().split(',')
        # Clean the list
        services_list = [service.strip() for service in services_list if service.strip()]
        return services_list
    except Exception as e:
        st.error(f"An error occurred while identifying AWS services: {e}")
        return []

def append_summary_to_file(summary, title, url, category, tags):
    with open("summaries.txt", "a", encoding="utf-8") as file:
        file.write(f"Title: {title}\nURL: {url}\nSummary: {summary}\nCategory: {category}\nTags: {', '.join(tags)}\n\n")

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
    
def download_video(url):
    try:
        yt = YouTube(url)
        video = yt.streams.filter(file_extension='mp4', progressive=True).order_by('resolution').desc().first()
        if video:
            st.info(f"Downloading video: {yt.title}")
            safe_filename = ''.join(char for char in yt.title if char.isalnum() or char in " -_").rstrip()
            video.download(output_path='videos', filename=f"{safe_filename}.mp4")
            st.success("Download complete!")
            return os.path.join('videos', f"{safe_filename}.mp4"), yt.title
        else:
            st.error("No downloadable video found.")
            return None, None
    except Exception as e:
        st.error(f"An error occurred while downloading the video: {e}")
        return None, None

def summarize_transcript(transcript):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "Summarize the transcript into 3 or 4 sentences."}, {"role": "user", "content": transcript}]
        )
        summary = response.choices[0].message.content.strip()
        category = predict_category(summary)
        tags = identify_aws_services(summary)
        return summary, category, tags
    except Exception as e:
        st.error(f"An error occurred with the OpenAI API: {e}")
        return None, "Unknown", []

def youtube_processor():
    st.title("YouTube Video and Transcript Processor")
    video_url = st.text_input("Enter the YouTube video URL")
    if st.button("Process Video"):
        if video_url:
            video_id = YouTube(video_url).video_id
            yt = YouTube(video_url)
            try:
                transcript_text = check_and_download_transcript(video_id)
                if transcript_text:
                    st.text_area("Transcript", transcript_text, height=300)
                    summary, category, tags = summarize_transcript(transcript_text)
                    if summary:
                        formatted_text = f"- [{yt.title}]({video_url}) - {summary}\n\nCategory: {category}\nTags: {', '.join(tags)}"
                        st.markdown(formatted_text, unsafe_allow_html=True)
                        copy_text = f"- {yt.title} ({video_url}) - {summary}\n\nCategory: {category}\nTags: {', '.join(tags)}"
                        st.text_area("Copy the text below:", copy_text, height=100)
                        append_summary_to_file(summary, yt.title, video_url, category, tags)
            except Exception as e:
                st.error(f"An error occurred: {e}")
        else:
            st.warning("Please enter a YouTube URL.")

def content_summarizer():
    st.title("Content Summarizer")
    url = st.text_input("Enter the URL to summarize")
    if st.button("Summarize Content"):
        if url:
            try:
                headers = {'User-Agent': 'Mozilla/5.0'}
                response = requests.get(url, headers=headers)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'html.parser')
                page_title = soup.title.string if soup.title else "Article"
                paragraphs = soup.find_all('p')
                text_content = ' '.join([p.get_text() for p in paragraphs])
                os.makedirs('scraped_content', exist_ok=True)
                filename = re.sub(r'\W+', '_', url)[:255]
                with open(f"scraped_content/{filename}.txt", "w", encoding="utf-8") as file:
                    file.write(text_content)
                summary, category, tags = summarize_transcript(text_content)
                if summary:
                    st.write("Summary:")
                    st.write(summary)
                    copy_text = f"* [{page_title}]({url}) - {summary}\n\nCategory: {category}\nTags: {', '.join(tags)}"
                    st.text_area("Copy the Markdown text below:", copy_text, height=150)
                    append_summary_to_file(summary, page_title, url, category, tags)
            except Exception as e:
                st.error(f"An error occurred: {e}")
        else:
            st.warning("Please enter a valid URL.")

# Sidebar navigation
st.sidebar.title('Navigation')
page = st.sidebar.radio('Go to', ['YouTube Summarizer', 'Blog Article Summarizer', 'My Links'])

if page == 'My Links':
    st.sidebar.markdown('[Blog](https://brandonjcarroll.com)')
    st.sidebar.markdown('[GitHub](https://github.com/8carroll)')
    st.sidebar.markdown('[Socials](https://brandonjcarroll.com/bio)')

# Page functionality
if page == 'YouTube Summarizer':
    youtube_processor()
elif page == 'Blog Article Summarizer':
    content_summarizer()

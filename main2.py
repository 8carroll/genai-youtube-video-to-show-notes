import os
import re

import streamlit as st
import openai
from dotenv import load_dotenv
from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter

# Import the libraries for the web scraping
import requests
from bs4 import BeautifulSoup


# Load environment variables from .env file
load_dotenv()

# Use the API key from the .env file
openai.api_key = os.getenv('OPENAI_API_KEY')

# Ensure the 'videos' and 'transcripts' directories exist
os.makedirs('videos', exist_ok=True)
os.makedirs('transcripts', exist_ok=True)

# Function to check and download the transcript
def check_and_download_transcript(video_id):
    try:
        # Fetch the transcript
        transcript = YouTubeTranscriptApi.get_transcript(video_id)

        # Format the transcript into plain text
        formatter = TextFormatter()
        transcript_text = formatter.format_transcript(transcript)

        # Save the transcript to a file
        with open(f'transcripts/{video_id}.txt', 'w', encoding='utf-8') as file:
            file.write(transcript_text)

        st.success("Transcript downloaded successfully.")
        return transcript_text
    except Exception as e:
        st.warning("No transcript available or an error occurred.")
        return None
    

# Function to download the video
def download_video(url):
    try:
        yt = YouTube(url)
        video = yt.streams.filter(file_extension='mp4', progressive=True).order_by('resolution').desc().first()
        if video:
            st.info(f"Downloading video: {yt.title}")
            safe_filename = ''.join(char for char in yt.title if char.isalnum() or char in " -_").rstrip()
            video.download(output_path='videos', filename=f"{safe_filename}.mp4")
            st.success("Download complete!")
            download_path = os.path.join('videos', f"{safe_filename}.mp4")
            return download_path, yt.title  # Return the download path and video title
        else:
            st.error("No downloadable video found.")
            return None, None
    except Exception as e:
        st.error(f"An error occurred while downloading the video: {e}")
        return None, None


# Function to summarize the transcript
def summarize_transcript(transcript):
    try:
        # Call the OpenAI API with the transcript and summarization prompt
        response = openai.chat.completions.create(model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes text."},
            {"role": "user", "content": f"When you provide a response, do so as if you are sharing a summary of a video you wantched with a reader of your newsletter.  You should encourage them to check out the video. Summarize the following transcript into 3 or 4 sentences:\n\n{transcript}"}
        ])
        summary = response.choices[0].message.content.strip()
        return summary
    except Exception as e:
        st.error(f"An error occurred with the OpenAI API: {e}")
        return None



def youtube_processor():
    st.title("YouTube Video and Transcript Processor")

    # Input field for YouTube video URL
    video_url = st.text_input("Enter the YouTube video URL")

    # Button to process the video
    if st.button("Process Video"):
        if video_url:
            video_id = YouTube(video_url).video_id
            yt = YouTube(video_url)  # Get YouTube object to access the title
            try:
                transcript_text = check_and_download_transcript(video_id)

                if transcript_text:
                    st.text_area("Transcript", transcript_text, height=300)
                    summary = summarize_transcript(transcript_text)
                    if summary:
                        # Display the video title, URL, and summary in formatted markdown
                        formatted_text = f"- [{yt.title}]({video_url}) - {summary}"
                        st.markdown(formatted_text, unsafe_allow_html=True)
                        
                        # Provide the same text in a text area for easy manual copying
                        copy_text = f"- {yt.title} ({video_url}) - {summary}"
                        st.text_area("Copy the text below:", copy_text, height=100)
                else:
                    st.warning("No transcript is available for this video. Starting download...")
                    download_path, video_title = download_video(video_url)
                    if download_path:
                        st.info(f"Video has been downloaded to: {download_path}")
                    else:
                        st.error("Failed to download the video.")
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
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

                # Fetch the content from the URL with headers
                response = requests.get(url, headers=headers)
                response.raise_for_status()  # Raise an exception for HTTP errors

                # Parse the HTML content
                soup = BeautifulSoup(response.text, 'html.parser')

                # Extract the title of the article
                page_title = soup.title.string if soup.title else "Article"

                # Extract text from paragraph tags
                paragraphs = soup.find_all('p')
                text_content = ' '.join([p.get_text() for p in paragraphs])

                # Ensure the 'scraped_content' directory exists
                os.makedirs('scraped_content', exist_ok=True)

                # Sanitize the filename derived from the URL
                filename = re.sub(r'\W+', '_', url)[:255]  # Replace non-alphanumeric characters with underscores and limit length

                # Save the scraped content to a file
                with open(f"scraped_content/{filename}.txt", "w", encoding="utf-8") as file:
                    file.write(text_content)

                # Adjusting the prompt for summarization
                prompt_text = f"The following content has been extracted from a blog post at {url}. Please summarize it in 3 or 4 sentences:\n\n{text_content}"

                # Call the OpenAI API to summarize the extracted text
                summary = summarize_transcript(prompt_text)

                if summary:
                    st.write("Summary:")
                    st.write(summary)

                    # Format the URL and summary for Markdown with the article title
                    copy_text = f"* [{page_title}]({url}) - {summary}"
                    st.text_area("Copy the Markdown text below:", copy_text, height=150)
                else:
                    st.error("Failed to generate a summary.")
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

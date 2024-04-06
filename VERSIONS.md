# Version Explainations

## summarize-and-service-tags.py

This code is a Streamlit application that provides two main functionalities:

1. **YouTube Video and Transcript Processor**:
   - The user can input a YouTube video URL.
   - The application downloads the video transcript (if available) using the `youtube_transcript_api` library.
   - It generates a summary of the transcript using the OpenAI GPT-3.5-turbo model.
   - The summary is categorized as either "Technical Topic," "Career Advice," or "Certification and Learning" using the OpenAI model.
   - The application also identifies any AWS services mentioned in the summary.
   - The summary, category, tags (AWS services), title, and URL are displayed to the user and appended to a "summaries.txt" file.
   - The user can optionally download the video using the `pytube` library.

2. **Content Summarizer**:
   - The user can input a URL of a website or blog article.
   - The application scrapes the content from the URL using the `requests` and `BeautifulSoup` libraries.
   - It generates a summary of the scraped content using the OpenAI GPT-3.5-turbo model.
   - The summary is categorized, and AWS services are identified, similar to the YouTube processor.
   - The summary, category, tags, title, and URL are displayed to the user and appended to the "summaries.txt" file.

The code also includes a sidebar navigation where the user can switch between the "YouTube Summarizer" and "Blog Article Summarizer" pages. Additionally, there's a "My Links" page that displays some personal links.

The application uses the following libraries:

- `os`: for interacting with the operating system
- `re`: for regular expression operations
- `streamlit`: for building the web application
- `openai`: for using the OpenAI GPT-3.5-turbo model
- `dotenv`: for loading environment variables from a `.env` file
- `requests`: for making HTTP requests
- `BeautifulSoup`: for web scraping
- `pytube`: for downloading YouTube videos
- `youtube_transcript_api`: for retrieving YouTube video transcripts

The code also creates the necessary directories ("videos", "transcripts", and "scraped_content") if they don't exist.

## summarizer-with-category.py

This code is a Streamlit application that provides two main functionalities: YouTube Video and Transcript Processor, and Content Summarizer. Let's break it down:

1. **YouTube Video and Transcript Processor**:
   - The user can input a YouTube video URL.
   - The application downloads the video transcript (if available) using the `youtube_transcript_api` library.
   - It generates a summary of the transcript using the OpenAI GPT-3.5-turbo model.
   - The summary is categorized as either "Technical Topic," "Career Advice," or "Certification and Learning" using the OpenAI model and the `predict_category` function.
   - The summary, category, title, and URL are displayed to the user and appended to a "summaries.txt" file using the `append_summary_to_file` function.
   - The user can optionally download the video using the `pytube` library and the `download_video` function.

2. **Content Summarizer**:
   - The user can input a URL of a website or blog article.
   - The application scrapes the content from the URL using the `requests` and `BeautifulSoup` libraries.
   - It generates a summary of the scraped content using the OpenAI GPT-3.5-turbo model and the `summarize_transcript` function.
   - The summary is categorized, similar to the YouTube processor.
   - The summary, category, title, and URL are displayed to the user and appended to the "summaries.txt" file using the `append_summary_to_file` function.

The code also includes a sidebar navigation where the user can switch between the "YouTube Summarizer" and "Blog Article Summarizer" pages. Additionally, there's a "My Links" page that displays some personal links.

The application uses the following libraries:

- `os`: for interacting with the operating system
- `re`: for regular expression operations
- `streamlit`: for building the web application
- `openai`: for using the OpenAI GPT-3.5-turbo model
- `dotenv`: for loading environment variables from a `.env` file
- `requests`: for making HTTP requests
- `BeautifulSoup`: for web scraping
- `pytube`: for downloading YouTube videos
- `youtube_transcript_api`: for retrieving YouTube video transcripts

The code also creates the necessary directories ("videos", "transcripts", and "scraped_content") if they don't exist.

The main difference from the previous version is the removal of the `identify_aws_services` function, which was responsible for identifying AWS services mentioned in the summary.


## summarizer-yt-blog.py

This code is a Streamlit application that provides two main functionalities: YouTube Video and Transcript Processor, and Content Summarizer. Let's break it down:

1. **YouTube Video and Transcript Processor**:
   - The user can input a YouTube video URL.
   - The application downloads the video transcript (if available) using the `youtube_transcript_api` library.
   - It generates a summary of the transcript using the OpenAI GPT-3.5-turbo model and the `summarize_transcript` function.
   - The summary is formatted with the video title and URL, and displayed to the user.
   - If no transcript is available, the application offers to download the video using the `pytube` library and the `download_video` function.
   - The summary, video title, and URL are appended to a "summaries.txt" file using the `append_summary_to_file` function.

2. **Content Summarizer**:
   - The user can input a URL of a website or blog article.
   - The application scrapes the content from the URL using the `requests` and `BeautifulSoup` libraries.
   - It extracts the page title and text content from the HTML.
   - The text content is saved to a file in the "scraped_content" directory.
   - The application generates a summary of the text content using the OpenAI GPT-3.5-turbo model and the `summarize_transcript` function.
   - The summary is displayed to the user, along with the page title and URL in Markdown format.
   - The summary, page title, and URL are appended to the "summaries.txt" file using the `append_summary_to_file` function.

The code also includes a sidebar navigation where the user can switch between the "YouTube Summarizer" and "Blog Article Summarizer" pages. Additionally, there's a "My Links" page that displays some personal links.

The application uses the following libraries:

- `os`: for interacting with the operating system
- `re`: for regular expression operations
- `streamlit`: for building the web application
- `openai`: for using the OpenAI GPT-3.5-turbo model
- `dotenv`: for loading environment variables from a `.env` file
- `requests`: for making HTTP requests
- `BeautifulSoup`: for web scraping
- `pytube`: for downloading YouTube videos
- `youtube_transcript_api`: for retrieving YouTube video transcripts

The code also creates the necessary directories ("videos", "transcripts", and "scraped_content") if they don't exist.

A notable change from the previous version is the use of the OpenAI `chat.completions` endpoint for summarization, which allows for more flexible and contextual prompts.

## summarizer.py

This code is a Streamlit application that allows users to process YouTube videos and download their transcripts, as well as summarize the transcripts using OpenAI's GPT-3.5-turbo model. Here's a breakdown of what the code does:

1. **Load Environment Variables**: The code loads environment variables from a `.env` file using the `dotenv` library and sets the OpenAI API key from the loaded environment variables.

2. **Sidebar**: The code creates a sidebar in the Streamlit app with links to the developer's blog, GitHub, and social media profiles.

3. **Create Directories**: It creates the `videos` and `transcripts` directories if they don't exist, to store downloaded videos and transcripts, respectively.

4. **Check and Download Transcript**: The `check_and_download_transcript` function checks if a transcript is available for a given YouTube video ID, downloads it, saves it in the `transcripts` directory, and returns the transcript text.

5. **Download Video**: The `download_video` function downloads the highest-resolution, progressive MP4 video from a given YouTube URL, saves it in the `videos` directory, and returns the download path and video title.

6. **Summarize Transcript**: The `summarize_transcript` function takes a transcript text as input and uses the OpenAI GPT-3.5-turbo model to generate a summary of the transcript. It formats the summary as if it were a newsletter or blog post describing the video and encouraging readers to watch it.

7. **Streamlit UI**: The code sets up the Streamlit user interface with a title and a text input field for entering a YouTube video URL. When the user clicks the "Process Video" button, the following happens:
   - If a valid YouTube URL is provided, the code retrieves the video ID and creates a `YouTube` object from the URL.
   - It attempts to download the transcript using the `check_and_download_transcript` function.
   - If a transcript is available, it displays the transcript text in a text area and generates a summary using the `summarize_transcript` function.
   - The video title, URL, and summary are displayed in formatted Markdown, and the user can copy the formatted text from a text area.
   - If no transcript is available, the code offers to download the video using the `download_video` function and displays the download path if successful.
   - If any exceptions occur during the process, error messages are displayed in the Streamlit app.

The code uses the following libraries:

- `os`: for interacting with the operating system
- `streamlit`: for building the web application
- `openai`: for using the OpenAI GPT-3.5-turbo model
- `dotenv`: for loading environment variables from a `.env` file
- `pytube`: for downloading YouTube videos
- `youtube_transcript_api`: for retrieving YouTube video transcripts

Overall, this Streamlit application provides a user-friendly interface for processing YouTube videos, downloading transcripts, and generating summaries using OpenAI's language model.
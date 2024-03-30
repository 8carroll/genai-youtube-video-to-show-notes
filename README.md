# YouTube and Blog Summarization App

This repository contains a Streamlit application that provides two main functionalities:
1. Summarizing YouTube videos by downloading their transcripts.
2. Scraping web articles and summarizing their content.

## Features

- **YouTube Video Summarizer:** Enter a YouTube video URL to fetch its transcript and generate a summary.
- **Blog Article Summarizer:** Enter the URL of a blog article to scrape its content and generate a summary.

## How to Use

### Cloning the Repository

To get started, clone this repository to your local machine by running:

```bash
git clone https://github.com/8carroll/youtube-video-summarizer.git
cd youtube-video-summarizer
```

### Setting Up a Virtual Environment

It's recommended to run this application within a virtual environment. If you don't have `virtualenv` installed, you can install it using pip:

```bash
pip install virtualenv
```

Create and activate a virtual environment:

- **For Windows:**

```bash
virtualenv myvenv
.\myvenv\Scripts\activate
```

- **For macOS and Linux:**

```bash
virtualenv myvenv
source myvenv/bin/activate
```

### Installing Dependencies

Install the required Python packages using:

```bash
pip install -r requirements.txt
```

### Running the Application

Start the Streamlit application with:

```bash
streamlit run main2.py
```

### Interacting with the Web UI

1. **Navigate to the App URL:** Open your web browser and go to `http://localhost:8501` or the URL provided in the terminal after starting the app.
2. **Choose the Functionality:** Use the sidebar to select between the "YouTube Summarizer" and "Blog Article Summarizer".
3. **Enter a URL:** In the input field provided, enter the URL of a YouTube video or a blog article depending on the selected functionality.
4. **Generate Summary:** Click the "Process Video" or "Summarize Content" button to fetch and summarize the content.
5. **View and Copy Results:** The summary will be displayed below the button. You can also copy the Markdown-formatted summary from the provided text area.

## Contributing

Feel free to fork this repository and submit pull requests to contribute to this project. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)
```

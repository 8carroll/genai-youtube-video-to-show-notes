# YouTube Show Notes Generator

This Streamlit application automatically generates show notes from YouTube video transcripts using Amazon Bedrock's AI capabilities.

## Features

- **Transcript Fetching:** Automatically downloads transcripts from YouTube videos.
- **AI-Powered Summarization:** Utilizes Amazon Bedrock to create concise and informative show notes.
- **Easy-to-Use Interface:** Simple web interface for inputting YouTube URLs and viewing results.
- **Copy-Friendly Output:** Generates formatted show notes that are easy to copy and use.

## Prerequisites

- Python 3.7+
- An AWS account with access to Amazon Bedrock
- AWS CLI configured with appropriate credentials

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/8carroll/youtube-show-notes-generator.git
   cd youtube-show-notes-generator
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Ensure your AWS CLI is configured with credentials that have access to Amazon Bedrock.

## Running the Application

Launch the Streamlit app:

```bash
streamlit run show_notes_generator.py
```

## Usage

1. Open your web browser and go to the URL provided by Streamlit (typically `http://localhost:8501`).
2. Enter a YouTube video URL in the input field.
3. Click "Generate Show Notes" to process the video.
4. View the generated show notes and use the text area to copy them.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues to discuss potential improvements.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
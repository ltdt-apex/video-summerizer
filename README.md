# YouTube Video Summarizer

This project was born out of a curiosity to explore and understand how modern video summarization works. By combining YouTube's transcript API, OpenAI's Whisper for speech-to-text (as a fallback), and GPT for summarization, it demonstrates a practical implementation of current AI technologies to solve the common problem of quickly understanding video content.

The architecture showcases how different AI services can be chained together:
- YouTube's API provides native transcripts when available
- Whisper handles speech-to-text conversion when needed
- GPT processes the raw transcript into coherent, structured summaries

## Prerequisites

- OpenAI API key
- Docker and Docker Compose

## Setup

1. Clone the repository
   ```bash
   git clone https://github.com/ltdt-apex/video-summerizer.git
   cd video-summerizer
   ```

2. Create a `.env` file in the root directory:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

## Running the Application

<!-- ### Local Development

1. Start the backend server:
   ```bash
   cd backend
   uvicorn app.main:app --reload --port 8000
   ```

2. Start the frontend:
   ```bash
   cd frontend
   streamlit run app.py
   ```

3. Open your browser and navigate to `http://localhost:8501` -->

### Using Docker Compose

1. Build and start the containers:
   ```bash
   docker-compose up --build
   ```

2. Open your browser and navigate to `http://localhost:8501`

## Usage

1. Enter a YouTube URL in the chat input
2. Wait for the AI to process and generate the summary
3. View the embedded video and generated summary in the chat interface

## Technologies Used

- Frontend:
  - Streamlit
  - Python
  - YouTube Embed

- Backend:
  - FastAPI
  - pytube
  - OpenAI API

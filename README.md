# YouTube Video Summarizer

A web application that summarizes YouTube videos using LLM. The application features a ChatGPT-like interface where users can input a YouTube URL and receive an AI-generated summary of the video content.

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
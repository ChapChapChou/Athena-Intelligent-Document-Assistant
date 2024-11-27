# PDF Document Assistant

A tool for processing, chatting with PDF documents and generating cover images based on document content.

## Features

- 📚 PDF document processing and embedding
- 💬 Interactive chat with your PDF documents
- 🎨 Automatic cover image generation
- 🔍 Vector-based document search

## Installation

1. Clone the repository:
```bash
git clone
```
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Set AWS credentials:
```bash
chmod 777 set_env.sh
./set_env.sh
```
## Usage

—— Document Processing
Initialize the vector store with your PDF documents:
```bash
python init_vectorstore.py
```
This will automatically process and embed all PDF files located in the ./data directory.
 
—— Chat Interface
Start an interactive chat session with your documents:
```bash
python chat.py
```
Type your questions to get answers based on the PDF content
Type quit to exit the chat session
 
—— Cover Generation
Generate a cover image based on document summaries:
```bash
python generate_pic.py
```
This will automatically analyze your PDFs and create a relevant cover image.
## Directory Structure
```basic
.
├── data/           # Store your PDF files here
├── chat.py         # Chat interface
├── init_vectorstore.py    # Document processor
├── generate_pic.py # Cover generator
├── tranlate.py # translate text
├── set_env.sh # set aws credentials
└── requirements.txt
```

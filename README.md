📋 Prerequisites
Installing Ollama
Download and Install Ollama

# For Linux
curl -fsSL https://ollama.com/install.sh | sh

# For MacOS
brew install ollama
Start Ollama Service

ollama serve
Pull Llama3 Model

ollama pull llama3.2:1b
🚀 Project Setup
Create Virtual Environment

python3 -m venv venv
source venv/bin/activate  # On Linux/MacOS
# or
.\venv\Scripts\activate  # On Windows
Install Dependencies

pip3 install -r requirements.txt
Run the Application

python3 generate_devops-file.py

💡 How It Works
The script takes a programming language as input (e.g., Python, Node.js, Java)
Connects to the Ollama API running locally
Generates an optimized Dockerfile with best practices for the specified language
Returns the Dockerfile content with explanatory comments
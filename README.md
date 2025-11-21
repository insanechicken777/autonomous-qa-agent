🕷️ Autonomous QA Agent

An intelligent, full-stack AI agent capable of ingesting product documentation and HTML structure to autonomously generate comprehensive test plans and self-healing Selenium automation scripts.

📋 Project Overview
This system acts as an Autonomous SDET (Software Development Engineer in Test). It uses a RAG (Retrieval-Augmented Generation) pipeline to understand business rules from documentation and map them to the actual DOM elements of a target web application.
Key Features:
RAG Knowledge Base: Ingests Markdown and Text files to understand product specs.
Test Strategy Generation: AI creates positive, negative, and edge-case test scenarios.
Automated Scripting: Generates runnable Python Selenium scripts with dynamic waits and math verification.
Red Ops UI: A dark-mode, tactical interface built with Streamlit.

⚙️ Setup Instructions
1. Prerequisites
Python 3.10+ (Recommended for library compatibility)
Google Chrome (For Selenium execution)
2. Installation
Clone the repository and set up the environment:
# 1. Clone the repo
git clone https://github.com/insanechicken777/autonomous-qa-agent.git
cd autonomous-qa-agent

# 2. Create Virtual Environment
python -m venv venv

# 3. Activate Environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 4. Install Dependencies
pip install -r requirements.txt


The content you provided is the complete text for your README.md file. It is structured correctly, formatted well, and covers all the requirements for your assignment submission.
You can now simply:
Copy the text block below (I have formatted it one last time to ensure all Markdown syntax is perfect).
Paste it into your README.md file in VS Code.
Save the file.
Commit & Push to GitHub (git add README.md, git commit -m "Finalize documentation", git push).
🕷️ Autonomous QA Agent (Red Ops Edition)
An intelligent, full-stack AI agent capable of ingesting product documentation and HTML structure to autonomously generate comprehensive test plans and self-healing Selenium automation scripts.
📋 Project Overview
This system acts as an Autonomous SDET (Software Development Engineer in Test). It uses a RAG (Retrieval-Augmented Generation) pipeline to understand business rules from documentation and map them to the actual DOM elements of a target web application.
Key Features:
RAG Knowledge Base: Ingests Markdown and Text files to understand product specs.
Test Strategy Generation: AI creates positive, negative, and edge-case test scenarios.
Automated Scripting: Generates runnable Python Selenium scripts with dynamic waits and math verification.
Red Ops UI: A dark-mode, tactical interface built with Streamlit.

⚙️ Setup Instructions
1. Prerequisites
Python 3.10+ (Recommended for library compatibility)
Google Chrome (For Selenium execution)

2. Installation
Clone the repository and set up the environment:
code
Bash
# 1. Clone the repo
git clone https://github.com/insanechicken777/autonomous-qa-agent.git
cd autonomous-qa-agent

# 2. Create Virtual Environment
python -m venv venv

# 3. Activate Environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 4. Install Dependencies
pip install -r requirements.txt


3. Environment Configuration
You must provide a Groq API Key for the LLM (Llama 3) to function.
Create a file named .env in the root directory (same level as main.py).
Add your key inside:
GROQ_API_KEY=gsk_your_actual_api_key_here

How to Run
The system requires two separate terminals running simultaneously (Backend API and Frontend UI).
Terminal 1: The Backend (FastAPI)
This powers the AI logic, Vector Database, and File Processing.

# Make sure venv is active
uvicorn backend.main:app --reload

Status: You should see "Application startup complete".
Port: Runs on http://127.0.0.1:8000.
Terminal 2: The Frontend (Streamlit)
This launches the "Red Ops" Dashboard.
# Open a new terminal, activate venv, then run:
streamlit run frontend/app.py
Status: Your browser should automatically open.
Port: Runs on http://localhost:8501.

Usage Examples (The "Happy Path")
Follow this workflow to test the system capabilities:
Phase 1: Ingestion
Go to the "INGESTION (SETUP)" tab.
Support Documents: Drag & drop assets/product_specs.md and assets/ui_ux_guide.txt.
Target Application: Drag & drop assets/checkout.html.
Click "INITIALIZE KNOWLEDGE BASE".
Result: Green success message confirming the Vector DB has been built.
Phase 2: Test Planning
Switch to the "AGENT (EXECUTION)" tab.
Enter a query: "Generate test cases for the discount code SAVE15 and Free Shipping logic."
Click "EXECUTE PLAN".
Result: A structured table displays test scenarios (e.g., TC-001) referencing the uploaded docs.
Phase 3: Script Generation & Execution
Select a specific case from the dropdown (e.g., "Apply valid discount code SAVE15").
Click "GENERATE PAYLOAD (PYTHON SCRIPT)".
The AI will generate code that:
Adds items to the cart (because the default cart is empty).
Calculates the expected price dynamically ($150 * 0.85).
Waits for the JavaScript to update.
Run the Script:
Download the script or copy it to a file named test_run.py.
Run it in your terminal:
code
Bash
python test_run.py
Result: Chrome opens, performs the test, and the terminal prints "✅ ASSERTION PASSED".
📂 Included Support Documents
The assets/ folder contains the testing artifacts used to train the agent:
File	Purpose	Key Logic Contained
checkout.html	Target App	The single-page application under test. It includes JavaScript logic for calculating totals, handling shipping costs ($10 vs Free), and validation errors. Note: Default item quantity is set to 0 to allow "Empty Cart" testing.
product_specs.md	Business Rules	Defines the core logic: <br> - Code "SAVE15" gives 15% off.<br> - Code "FREESHIP" removes shipping costs.<br> - Express shipping costs $10.
ui_ux_guide.txt	Visual Rules	Defines how the app should look:<br> - "Pay Now" button must be Green.<br> - Error messages must be Red.<br> - Success messages must be visible.
📂 Project Structure
code
Text
qa_agent/
├── assets/              # Test artifacts (HTML, Docs, Images)
├── backend/             # FastAPI Server & RAG Logic
├── frontend/            # Streamlit Dashboard
├── vector_db/           # Local Vector Storage (ChromaDB)
├── main.py              # Backend Entry Point
└── app.py               # Frontend Entry Point
🛠️ Tech Stack
Backend: FastAPI, LangChain, ChromaDB
Frontend: Streamlit (Custom CSS)
AI Model: Llama-3 (via Groq Cloud)
Automation: Selenium WebDriver (Python)

Built for Autonomous QA Agent Assignment.
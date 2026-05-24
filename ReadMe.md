# AI Customer Support Workflow using LangGraph

This project is an AI-powered customer support workflow for Bloom Aesthetics Clinic built using LangGraph and LangChain.

The system handles FAQ answering, lead qualification, escalation detection, and conversation summarization using LLM-based routing and state management.

## Features

- SOP-based FAQ answering
- Lead qualification workflow
- Escalation detection
- Conversation summarization
- Multi-node LangGraph workflow
- Structured JSON outputs

## WORKFLOW DESIGN
```

                                        START
                                          ↓
                                        FAQ_node
                                          ↓
                                    ┌───────────────┐
                                    ↓               ↓
                                Lead_node     Escal_node
                                    ↓               ↓
                                    Convo_node <────┘
                                        ↓
                                       END
```
## Project Structure
---
          project/
               │
               |── main/
               |    |
               |    | 
               |    |── graph.py
               |    |── nodes.py
               |    |── prompts.md
               |    |── prompts.py
               |    └── state.py
               |── Test/
               |    |
               |    |── Abusive_Escalation.txt
               |    |── IN_SOP.txt
               |    └── Out_of_scop.txt
               |    
               |── LICENSE
               |── Readme.md
               └── requirements.txt
---


## Tech Stack

- Python
- LangGraph
- LangChain
- Groq API
- Anthropic API
- Pydantic
---

## Setup Instructions
### 1. Clone the Repository
git clone https://github.com/akshatavyas01-byte/AI-Customer-Support-Workflow-using-LangGraph.git
cd Support_workflow
### 2. Create Virtual Environment
python -m venv .venv

### Activate environment:
1. Windows
.venv\Scripts\activate

2. Mac/Linux
source .venv/bin/activate

### 3. Install Dependencies
pip install -r requirements.txt

### 4. Create .env File
groq_api=YOUR_GROQ_API_KEY
anthro=YOUR_ANTHROPIC_API_KEY

---

### Dependencies

- langgraph
- langchain
- langchain-groq
- langchain-anthropic
- python-dotenv
- pydantic

## How to Run the Workflow

- Run the graph workflow:
```python
python graph.py
```
The workflow starts from the FAQ node and routes dynamically based on user interaction.

## Known Limitations / Trade-offs
- Sometimes the LLM can hallucinate and route to wrong nodes.
- JSON parsing may fail occasionally if the model does not return proper JSON format.
- Conversation history is stored only during runtime and not in a database.
- Escalation system is simulated and does not connect to a real human support team.
- The project currently uses Groq models for testing because Anthropic free usage was limited.
- No authentication, user management, or persistent chat storage is implemented yet.
- The workflow currently runs through terminal interaction only and does not have a frontend/UI.

## Author
**Akshata Vyas**  
GitHub: [akshatavyas01-byte](https://github.com/akshatavyas01-byte)


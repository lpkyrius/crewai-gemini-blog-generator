# CrewAI Multiagent Examples

A collection of advanced, real-world multi-agent [CrewAI](https://github.com/crewAIInc/crewAI) workflows for business automation-featuring customer support, event planning, financial analysis, and sales/outreach, all powered by OpenAI and integrated with web search and scraping tools.

---

## 🚀 What’s Inside

- **Customer Support Automation:** Multi-agent support and QA with web tools.
- **Customer Outreach Campaigns:** Lead profiling, personalized outreach, and sentiment analysis.
- **Event Planning Automation:** Venue coordination, logistics, and marketing agents.
- **Financial Analysis Collaboration:** Data analysis, strategy, execution, and risk assessment agents.
- **Modular, extensible code:** Each workflow is a standalone Python script, ready for customization.

---

## 📁 Project Structure
```
.
├── L3_customer_support.py
├── L4_customer_outreach.py
├── L5_event_planning.py
├── L6_financial_analysis.py
├── utils.py
├── requirements.txt
└── README.md
```

---

## 🛠️ Getting Started

### 1. Clone the Repository

```
git clone https://github.com/your-username/crewai-multiagent-examples.git
cd crewai-multiagent-examples
```


### 2. Install Dependencies

```pip install -r requirements.txt```

Or, if you don’t have a `requirements.txt`:

```
pip install crewai crewai_tools langchain_community python-dotenv openai
```


### 3. Set Up API Keys

Create a `.env` file in the project root with:
```
OPENAI_API_KEY=your-openai-api-key
SERPER_API_KEY=your-serper-api-key
```


- [How to get an OpenAI API key](https://platform.openai.com/api-keys)
- [How to get a Serper API key](https://serper.dev/)

### 4. Run a Workflow

Pick any script (e.g., event planning):

```python L5_event_planning.py```


Follow prompts for human input if required. Results and output files will be printed in your terminal.

---

## 🧩 Workflows Overview

| Script                  | Description                                 |
|-------------------------|---------------------------------------------|
| L3_customer_support.py  | Automated customer support & QA agents      |
| L4_customer_outreach.py | Lead profiling & outreach campaign agents   |
| L5_event_planning.py    | Event planning with venue, logistics, marketing agents |
| L6_financial_analysis.py| Financial analysis with trading, risk, and execution agents |

---

## 📝 Customization

- **Change agent prompts, roles, or tools** in each script to fit your use case.
- **Add your own tools** (e.g., CRM, custom APIs) using CrewAI’s tool interface.
- **Switch LLM models** by editing the `OPENAI_MODEL_NAME` environment variable.

---

## 🤝 Contributing

Pull requests and issues are welcome! Please open an issue to discuss changes or ideas.

---

## 📄 License

MIT License

---

## 🙏 Acknowledgments

- [CrewAI](https://github.com/crewAIInc/crewAI)
- [OpenAI](https://platform.openai.com/)
- [Serper](https://serper.dev/)
- [LangChain Community](https://github.com/langchain-ai/langchain)

---

**Empower your business automation with multi-agent CrewAI workflows!**

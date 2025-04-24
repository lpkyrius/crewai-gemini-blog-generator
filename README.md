# CrewAI Blog Generator with Google Gemini

This project demonstrates how to use [CrewAI](https://github.com/crewAIInc/crewAI) with [Google Gemini](https://ai.google.dev/) as the language model to automatically plan, write, and edit high-quality blog posts on any topic. The workflow is modular, with distinct agents for content planning, writing, and editing—each powered by Google Gemini’s state-of-the-art generative AI.

---

## Features

- **Multi-Agent Workflow:** Planner, Writer, and Editor agents collaborate to produce professional blog content.
- **Google Gemini Integration:** Uses Gemini’s free API (within quota) for all text generation.
- **Modular Tasks:** Each agent is assigned a clear, realistic role and task.
- **Markdown Output:** Final blog post is ready for publication.

---

## Getting Started

### 1. Clone the Repository

git clone https://github.com/your-username/crewai-gemini-blog-generator.gitcd crewai-gemini-blog-generator


### 2. Install Dependencies

Make sure you have Python 3.9+ installed.

```
pip install -r requirements.txt
```


If you don’t have a `requirements.txt`, use:

```
pip install crewai crewai_tools langchain-google-genai python-dotenv
```


### 3. Set Up Your Google Gemini API Key

1. Get your API key from [Google AI Studio](https://aistudio.google.com/).
2. Create a `.env` file in the project root:

    ```
    GOOGLE_API_KEY=your-gemini-api-key-here
    ```

### 4. Run the Project

Edit `main.py` to set your desired topic, then run:

```
python main.py
```


The generated blog post will be printed in your terminal.

---

## Project Structure

```
.
├── main.py
├── .env
├── requirements.txt
└── README.md
```

---

## Example Output

Artificial Intelligence
Introduction
Artificial Intelligence (AI) is transforming industries…
Latest Trends and Key Players
…
Conclusion
…


---

## Customization

- **Change the topic:** Edit the `topic` variable in `main.py`.
- **Adjust agent prompts:** Modify agent definitions in `main.py` for different writing styles or workflows.
- **Switch Gemini models:** Change the `model` parameter in the LLM setup (e.g., `"gemini-1.5-flash"` or `"gemini-pro"`).

---

## License

This project is licensed under the [MIT License](LICENSE).

---

## Credits

- [DeepLearning](https://learn.deeplearning.ai/)
- [CrewAI](https://github.com/crewAIInc/crewAI)
- [Google Gemini](https://ai.google.dev/)
- [LangChain Google GenAI](https://github.com/langchain-ai/langchain)

---

## Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

---

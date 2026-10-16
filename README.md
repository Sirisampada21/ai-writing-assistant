# AI Writing Assistant

A beginner-friendly Streamlit app that generates:
- Blog posts
- Professional emails
- Code explanations
- Social media posts

Features:
- OpenAI or Google Gemini provider selection
- A reusable prompt template for each task
- Adjustable temperature and output-token limit
- Markdown, plain-text, and JSON output instructions
- Editable output and a download button

## 1. Requirements

Python 3.10 or newer and an API key for either OpenAI or Gemini.

## 2. Set up on macOS

Open Terminal and move into this project folder:

```bash
cd path/to/ai_writing_assistant
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 3. Configure an API key

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

Open `.env` in VS Code and replace the placeholder with your own API key. You only need the key for the provider you plan to use. Keep `.env` private and never upload it to GitHub.

## 4. Run the app

```bash
streamlit run app.py
```

A local address will appear in Terminal (usually `http://localhost:8501`). Open it in your browser.

## 5. Use it

1. Select OpenAI or Gemini in the sidebar.
2. Choose a task template.
3. Enter the topic or source content and optional instructions.
4. Adjust tone, audience, length, temperature, and output format.
5. Click **Generate content**. Edit the result or download it.

## Notes

- API usage may incur charges depending on your account and model.
- Model names and parameter support can change; use a model available to your API key.
- JSON mode is requested through the prompt in this starter app, so always validate the result before using it in another system.
- The app displays provider errors to help with setup. Avoid pasting secrets or sensitive personal information into prompts.

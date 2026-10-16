import os
from typing import Dict

import streamlit as st
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="AI Writing Assistant",
    page_icon="✍️",
    layout="wide",
)

PROMPTS: Dict[str, str] = {
    "Blog writing": """You are an experienced blog writer.
Create a useful, original blog post about the user's topic.
Follow the requested audience, tone, and length.
Use a clear title, an engaging introduction, descriptive Markdown headings,
short paragraphs, practical examples where useful, and a concise conclusion.
Do not invent statistics, sources, or quotes. Flag uncertainty when needed.""",
    "Email drafting": """You are a professional email-writing assistant.
Draft an email that matches the user's purpose, audience, and tone.
Include a relevant subject line, greeting, concise body, and appropriate sign-off.
Do not invent names, dates, promises, or facts that the user did not provide.
Use placeholders such as [Name] when details are missing.""",
    "Code explanation": """You are a patient programming tutor.
Explain the code or programming concept supplied by the user.
Organize the response into: Summary, How it works, Key lines/concepts,
Example (if useful), and Common pitfalls.
Use beginner-friendly language. If code is supplied, preserve its meaning,
do not claim to have executed it, and mention likely bugs or assumptions.""",
    "Social media post": """You are a creative social media copywriter.
Write a platform-appropriate post based on the user's brief.
Start with a strong hook, keep the message clear and engaging, and end with
a relevant call to action when appropriate. Suggest a few relevant hashtags
only if they fit naturally. Avoid misleading claims and engagement bait.""",
}

def generate_openai(prompt: str, temperature: float, model: str, max_tokens: int) -> str:
    from openai import OpenAI
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.responses.create(
        model=model,
        instructions=prompt,
        input=st.session_state.user_brief,
        temperature=temperature,
        max_output_tokens=max_tokens,
    )
    return response.output_text

def generate_gemini(prompt: str, temperature: float, model: str, max_tokens: int) -> str:
    from google import genai
    from google.genai import types
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    response = client.models.generate_content(
        model=model,
        contents=f"{prompt}\n\nUser request:\n{st.session_state.user_brief}",
        config=types.GenerateContentConfig(
            temperature=temperature,
            max_output_tokens=max_tokens,
        ),
    )
    return response.text or "The model returned an empty response."

st.title("✍️ AI Writing Assistant")
st.caption("Create blog posts, emails, code explanations, and social media content with reusable prompt templates.")

with st.sidebar:
    st.header("Generation settings")
    provider = st.selectbox("AI provider", ["OpenAI", "Gemini"])
    if provider == "OpenAI":
        model = st.text_input("Model", value=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
                              help="Use a model available to your OpenAI API key.")
        key_name = "OPENAI_API_KEY"
    else:
        model = st.text_input("Model", value=os.getenv("GEMINI_MODEL", "gemini-2.5-flash"),
                              help="Use a model available to your Gemini API key.")
        key_name = "GEMINI_API_KEY"

    temperature = st.slider(
        "Temperature", min_value=0.0, max_value=2.0, value=0.7, step=0.1,
        help="Lower values are more focused; higher values tend to be more varied. Provider/model support may differ."
    )
    max_tokens = st.slider("Maximum output tokens", 256, 8192, 2048, step=256)
    output_format = st.selectbox("Output format", ["Markdown", "Plain text", "JSON"])
    st.divider()
    st.caption("Your API key stays in your local environment when you run this app locally. Never commit keys to Git.")

left, right = st.columns([1, 1], gap="large")

with left:
    st.subheader("1. Describe what you need")
    content_type = st.selectbox("Writing task", list(PROMPTS.keys()))
    tone = st.selectbox("Tone", ["Professional", "Friendly", "Academic", "Persuasive", "Casual", "Creative"])
    audience = st.text_input("Target audience", placeholder="e.g., beginners, hiring manager, customers")
    length = st.selectbox("Length", ["Short", "Medium", "Long"])
    brief = st.text_area(
        "Topic, instructions, or source content",
        height=240,
        placeholder="Describe the topic, key points, context, and any requirements...",
    )
    extra = st.text_area(
        "Additional instructions (optional)",
        height=90,
        placeholder="e.g., include 3 headings, avoid jargon, use a CTA...",
    )

    generate = st.button("Generate content", type="primary", use_container_width=True)

with right:
    st.subheader("2. Generated result")
    if "generated_text" not in st.session_state:
        st.session_state.generated_text = ""
    if "user_brief" not in st.session_state:
        st.session_state.user_brief = ""

    if generate:
        if not brief.strip():
            st.warning("Please enter a topic or some content first.")
        elif not os.getenv(key_name):
            st.error(
                f"{key_name} is not set. Add your API key to a local .env file, then restart the app."
            )
        else:
            st.session_state.user_brief = (
                f"Task: {content_type}\n"
                f"Tone: {tone}\n"
                f"Target audience: {audience.strip() or 'Not specified'}\n"
                f"Desired length: {length}\n"
                f"Output format: {output_format}\n"
                f"Brief/source content:\n{brief.strip()}\n"
                f"Additional instructions:\n{extra.strip() or 'None'}\n\n"
                "Formatting rules: "
                + (
                    "Return valid JSON only. Use an appropriate object structure and no Markdown fences."
                    if output_format == "JSON"
                    else "Use Markdown formatting." if output_format == "Markdown"
                    else "Return plain text without Markdown headings or bullet syntax."
                )
            )
            with st.spinner(f"Generating with {provider}..."):
                try:
                    if provider == "OpenAI":
                        result = generate_openai(PROMPTS[content_type], temperature, model, max_tokens)
                    else:
                        result = generate_gemini(PROMPTS[content_type], temperature, model, max_tokens)
                    st.session_state.generated_text = result
                except Exception as exc:
                    st.error(f"Generation failed: {exc}")
                    st.caption("Check your API key, model name, internet connection, and provider quota.")

    if st.session_state.generated_text:
        st.text_area("Result (editable)", key="generated_text", height=420)
        st.download_button(
            "Download result",
            data=st.session_state.generated_text,
            file_name="ai_writing_result.txt",
            mime="text/plain",
            use_container_width=True,
        )
        if st.button("Clear result", use_container_width=True):
            st.session_state.generated_text = ""
            st.rerun()
    else:
        st.info("Your generated content will appear here.")

st.divider()
with st.expander("Prompt template preview"):
    st.code(PROMPTS.get(content_type, ""), language="text")

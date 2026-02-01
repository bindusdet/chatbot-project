import streamlit as st
import os

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# -----------------------------
# Streamlit Page Config
# -----------------------------
st.set_page_config(
    page_title="ITKannadigaru ChatBot",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 ITKannadigaru ChatBot")

# -----------------------------
# Sidebar Settings
# -----------------------------
st.sidebar.title("⚙️ Settings")

api_key = st.sidebar.text_input(
    "Enter your OpenAI API Key",
    type="password",
    help="Your OpenAI API key will be used only for this session"
)

temperature = st.sidebar.slider(
    "Temperature",
    min_value=0.0,
    max_value=1.0,
    value=0.7,
    step=0.1
)

max_tokens = st.sidebar.slider(
    "Max Tokens",
    min_value=50,
    max_value=500,
    value=150
)

model = st.sidebar.selectbox(
    "Select Model",
    [
        "gpt-4o-mini",   # Recommended
        "gpt-4o",
        "gpt-4-turbo",
        "gtp-5-mini"
    ]
)

# -----------------------------
# Prompt Template
# -----------------------------
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful AI assistant. Give clear, correct, and simple answers."),
        ("user", "{question}")
    ]
)

# -----------------------------
# Response Generator Function
# -----------------------------
def generate_response(question: str) -> str:
    llm = ChatOpenAI(
        api_key=api_key,
        model=model,
        temperature=temperature,
        max_tokens=max_tokens
    )

    chain = prompt | llm | StrOutputParser()
    return chain.invoke({"question": question})

# -----------------------------
# Main UI
# -----------------------------
st.write("### 💬 Ask your question")

user_question = st.text_input(
    "Type your question here:",
    placeholder="Example: Explain Kubernetes in simple words"
)

if user_question:
    if not api_key:
        st.warning("⚠️ Please enter your OpenAI API key in the sidebar.")
    else:
        try:
            with st.spinner("Thinking... 🤔"):
                answer = generate_response(user_question)
            st.success(answer)
        except Exception as e:
            st.error(f"❌ Error: {e}")
else:
    st.info("👆 Enter a question above to get started.")

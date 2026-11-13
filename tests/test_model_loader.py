
import os
import pytest
from dotenv import load_dotenv

from utils.model_loaders import ModelLoader


def test_groq_llm_connection():

    load_dotenv()

    # Check API key exists
    assert os.getenv("GROQ_API_KEY"), "GROQ_API_KEY is missing"

    # Load the LLM
    model_loader = ModelLoader(model_provider="groq")
    llm = model_loader.load_llm()

    # Send a real request to Groq
    response = llm.invoke("Say hello in one sentence.")

    # Verify response
    assert response is not None
    assert response.content

    print("Groq LLM response:", response.content)

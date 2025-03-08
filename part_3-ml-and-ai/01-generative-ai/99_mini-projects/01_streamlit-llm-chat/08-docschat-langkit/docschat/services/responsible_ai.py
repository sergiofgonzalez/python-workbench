"""Responsible AI service module."""

from enum import Enum

import streamlit as st
from langkit import extract, llm_metrics
from loguru import logger


class RAI(Enum):
    """Responsible AI metrics and text representations."""

    LANGKIT_PROMPT_JAILBREAK_SIMILARITY = "prompt.jailbreak_similarity"
    LANGKIT_PROMPT_TOXICITY = "prompt.toxicity"
    PROMPT_JAILBREAK_SIMILARITY_TEXT = "prompt.jailbreak_similarity.text"
    PROMPT_TOXICITY_TEXT = "prompt.toxicity.text"
    PROMPT_SECURITY_RISK = "prompt.security.risk"

    LANGKIT_RESPONSE_SENTIMENT = "response.sentiment_nltk"
    LANGKIT_RESPONSE_FLESCH_READING_EASE = "response.flesch_reading_ease"
    LANGKIT_RESPONSE_JAILBREAK_SIMILARITY = "response.jailbreak_similarity"
    LANGKIT_RESPONSE_REFUSAL_SIMILARITY = "response.refusal_similarity"
    LANGKIT_RESPONSE_TOXICITY = "response.toxicity"
    LANGKIT_RESPONSE_RELEVANCE_TO_PROMPT = "response.relevance_to_prompt"
    RESPONSE_SENTIMENT_POLARITY = "response.sentiment.polarity"
    RESPONSE_READING_EASE_TEXT = "response.flesch_reading_ease.text"
    RESPONSE_REFUSAL_SIMILARITY_TEXT = "response.refusal_similarity.text"
    RESPONSE_TOXICITY_TEXT = "response.toxicity.text"
    RESPONSE_RELEVANCE_TO_PROMPT_TEXT = "response.relevance_to_prompt.text"
    RESPONSE_SECURITY_RISK = "response.security.risk"


@st.cache_resource(show_spinner="Loading Responsible AI framework...")
def get_llm_schema():
    return llm_metrics.init()


# Force the schema to be loaded at the start of the app
LLM_SCHEMA = get_llm_schema()


def _get_text_from_rai_metric_value(value, mode):
    """Poor man's way of converting a metric value to a text representation."""
    text = str(value)
    if mode == "polarity":
        if value < 0:
            text = "negative"
        elif value == 0:
            text = "neutral"
        else:
            text = "positive"
    elif mode == "decimal":
        if value < 0.3:
            text = "low"
        elif value <= 0.7:
            text = "medium"
        else:
            text = "high"
    return text


def _summarize_security_prompt_metrics(rai_prompt_data) -> dict:
    """
    Poor man's way of creating custom metrics and adding them to the LLM schema
    metrics for the prompt.

    Take it as an example :)
    """
    logger.debug(
        "About to summarize security metrics in the prompt for '{}'",
        rai_prompt_data["prompt"],
    )
    jailbreak_similarity = _get_text_from_rai_metric_value(
        rai_prompt_data[RAI.LANGKIT_PROMPT_JAILBREAK_SIMILARITY.value],
        "decimal",
    )
    jailbreak_toxicity = _get_text_from_rai_metric_value(
        rai_prompt_data[RAI.LANGKIT_PROMPT_TOXICITY.value], "decimal"
    )

    rai_prompt_data[RAI.PROMPT_JAILBREAK_SIMILARITY_TEXT.value] = (
        jailbreak_similarity
    )
    rai_prompt_data[RAI.PROMPT_TOXICITY_TEXT.value] = jailbreak_toxicity

    logger.debug(
        "Security metrics for '{}': {}",
        rai_prompt_data["prompt"],
        rai_prompt_data,
    )
    return rai_prompt_data


def _summarize_rai_response_metrics(rai_response_data) -> dict:
    """
    Poor man's way of creating custom metrics and adding them to the LLM schema
    metrics for the response.

    Take it as an example :)
    """
    logger.debug(
        "About to summarize security metrics in the response: {}",
        rai_response_data["response"],
    )
    sentiment = _get_text_from_rai_metric_value(
        rai_response_data[RAI.LANGKIT_RESPONSE_SENTIMENT.value], "polarity"
    )
    reading_ease = _get_text_from_rai_metric_value(
        rai_response_data[RAI.LANGKIT_RESPONSE_FLESCH_READING_EASE.value],
        "polarity",
    )
    refusal_similarity = _get_text_from_rai_metric_value(
        rai_response_data[RAI.LANGKIT_RESPONSE_REFUSAL_SIMILARITY.value],
        "decimal",
    )
    toxicity = _get_text_from_rai_metric_value(
        rai_response_data[RAI.LANGKIT_RESPONSE_TOXICITY.value], "decimal"
    )
    relevance_to_prompt = _get_text_from_rai_metric_value(
        rai_response_data[RAI.LANGKIT_RESPONSE_RELEVANCE_TO_PROMPT.value],
        "decimal",
    )

    rai_response_data[RAI.RESPONSE_SENTIMENT_POLARITY.value] = sentiment
    rai_response_data[RAI.RESPONSE_READING_EASE_TEXT.value] = reading_ease
    rai_response_data[RAI.RESPONSE_REFUSAL_SIMILARITY_TEXT.value] = (
        refusal_similarity
    )
    rai_response_data[RAI.RESPONSE_TOXICITY_TEXT.value] = toxicity
    rai_response_data[RAI.RESPONSE_RELEVANCE_TO_PROMPT_TEXT.value] = (
        relevance_to_prompt
    )

    logger.debug(
        "Security metrics for '{}': {}",
        rai_response_data["response"],
        rai_response_data,
    )
    return rai_response_data


def _evaluate_prompt_security_risk(rai_prompt_data) -> dict:
    risk = 0
    for value in rai_prompt_data.values():
        if value == "high":
            risk += 1
    logger.debug(
        "Risk value for prompt '{}': {}", rai_prompt_data["prompt"], risk
    )
    rai_prompt_data[RAI.PROMPT_SECURITY_RISK.value] = (
        True if risk > 0 else False
    )
    return rai_prompt_data


def _evaluate_response_security_risk(rai_response_data) -> dict:
    if (
        rai_response_data[RAI.RESPONSE_TOXICITY_TEXT.value] == "high"
        or rai_response_data[RAI.RESPONSE_RELEVANCE_TO_PROMPT_TEXT.value]
        == "low"
        or rai_response_data[RAI.RESPONSE_REFUSAL_SIMILARITY_TEXT.value]
        == "high"
    ):
        rai_response_data[RAI.RESPONSE_SECURITY_RISK.value] = True
    else:
        rai_response_data[RAI.RESPONSE_SECURITY_RISK.value] = False
    return rai_response_data


def evaluate_prompt(prompt: str) -> dict:
    """
    Evaluate the security risk of a given prompt by calculating certain security
    metrics.

    Args:
        prompt (str): The prompt to evaluate.

    Returns:
        dict: A dictionary containing the prompt and the security risk metrics.
    """
    langkit_enhanced_prompt_data = extract(
        {"prompt": prompt}, schema=LLM_SCHEMA  # type: ignore
    )
    rai_summary_prompt_data = _summarize_security_prompt_metrics(
        langkit_enhanced_prompt_data
    )
    risk_assessed_prompt_data = _evaluate_prompt_security_risk(
        rai_summary_prompt_data
    )
    logger.debug("Enhanced prompt: {}", risk_assessed_prompt_data)
    return risk_assessed_prompt_data


def evaluate_response(prompt: str, response: str) -> dict:
    """
    Evaluate the security risk of a given response by calculating certain
    security metrics.

    Args:
        prompt (str): The prompt to evaluate.
        response (str): The response to evaluate.

    Returns:
        dict: A dictionary containing the prompt, the response and the security
        risk metrics.
    """
    langkit_enhanced_response_data = extract(
        {"prompt": prompt, "response": response},
        schema=LLM_SCHEMA,  # type: ignore
    )
    rai_summary_response_data = _summarize_rai_response_metrics(
        langkit_enhanced_response_data
    )
    risk_assessed_response_data = _evaluate_response_security_risk(
        rai_summary_response_data
    )
    logger.debug("Enhanced response: {}", risk_assessed_response_data)
    return risk_assessed_response_data

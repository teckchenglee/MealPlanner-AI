import streamlit as st

from llm import generate_json
from parse import parse_json_response
from prompts import build_steps_prompt, build_suggestions_prompt

def get_recipe_suggestions(client, mood, ingredients, tools, time_limit, extra_requests=None, previous_recipes=None):
    """Ask Gemini for 3 recipe suggestions, optionally refined by follow-up chat requests; returns a list or None on failure."""
    prompt = build_suggestions_prompt(mood, ingredients, tools, time_limit, extra_requests, previous_recipes)
    try:
        data = parse_json_response(generate_json(client, prompt))
        recipes = data.get("recipes", [])
        return recipes if recipes else None
    except Exception as exc:
        st.error(f"Sorry, we couldn't get recipe suggestions right now ({exc}). Please try again.")
        return None

def get_recipe_steps(client, recipe_name, mood, ingredients, tools, time_limit):
    """Ask Gemini for step-by-step instructions for one chosen recipe; returns a dict or None on failure."""
    prompt = build_steps_prompt(recipe_name, mood, ingredients, tools, time_limit)
    try:
        return parse_json_response(generate_json(client, prompt))
    except Exception as exc:
        st.error(f"Sorry, we couldn't get the recipe steps right now ({exc}). Please try again.")
        return None

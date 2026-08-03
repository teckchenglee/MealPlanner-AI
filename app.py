import streamlit as st

from analyzer import get_recipe_steps, get_recipe_suggestions
from llm import build_client, get_api_key


def init_session_state():
    """Set default session_state values on first run so later stages can rely on them existing."""
    defaults = {
        "stage": "input",
        "suggestions": None,
        "selected_recipe": None,
        "steps": None,
        "mood": "",
        "ingredients": "",
        "tools": "",
        "time_limit": 30,
        "chat_history": [],
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def render_input_stage(client):
    """Render the form that collects mood, ingredients, tools, and time limit from the user."""
    st.subheader("What are we working with today?")
    with st.form("planner_form"):
        mood = st.text_input("How are you feeling / what are you in the mood for?", placeholder="e.g. something comforting")
        ingredients = st.text_area("Ingredients available (comma-separated)", placeholder="e.g. eggs, rice, spinach, garlic")
        tools = st.text_input("Cooking tools available", placeholder="e.g. stovetop, microwave, oven")
        time_limit = st.number_input("Time limit (minutes)", min_value=5, max_value=180, value=30, step=5)
        submitted = st.form_submit_button("Find Recipes")

    if submitted:
        if not ingredients.strip():
            st.warning("Please list at least one ingredient.")
            return
        with st.spinner("Thinking of recipes..."):
            recipes = get_recipe_suggestions(client, mood, ingredients, tools, time_limit)
        if recipes:
            st.session_state.mood = mood
            st.session_state.ingredients = ingredients
            st.session_state.tools = tools
            st.session_state.time_limit = time_limit
            st.session_state.suggestions = recipes
            st.session_state.stage = "suggestions"
            st.rerun()


def render_suggestions_stage(client):
    """Render the list of suggested recipes, a chat box to refine them, and picking one to cook."""
    st.subheader("Here's what you could make:")
    for recipe in st.session_state.suggestions:
        with st.container(border=True):
            st.markdown(f"**{recipe.get('name', 'Untitled recipe')}** · ~{recipe.get('estimated_minutes', '?')} min")
            st.write(recipe.get("description", ""))
            if st.button("Cook this", key=f"pick_{recipe.get('name')}"):
                with st.spinner("Getting the steps ready..."):
                    steps = get_recipe_steps(
                        client,
                        recipe.get("name"),
                        st.session_state.mood,
                        st.session_state.ingredients,
                        st.session_state.tools,
                        st.session_state.time_limit,
                    )
                if steps:
                    st.session_state.steps = steps
                    st.session_state.stage = "steps"
                    st.rerun()

    if st.session_state.chat_history:
        with st.expander("Refinements applied so far"):
            for message in st.session_state.chat_history:
                st.markdown(f"- {message}")

    if st.button("Start over"):
        reset_to_input()
        st.rerun()

    chat_message = st.chat_input("Not quite right? e.g. \"I also have chicken\" or \"give me other options\"")
    if chat_message:
        st.session_state.chat_history.append(chat_message)
        with st.spinner("Updating suggestions..."):
            recipes = get_recipe_suggestions(
                client,
                st.session_state.mood,
                st.session_state.ingredients,
                st.session_state.tools,
                st.session_state.time_limit,
                extra_requests=st.session_state.chat_history,
                previous_recipes=st.session_state.suggestions,
            )
        if recipes:
            st.session_state.suggestions = recipes
            st.rerun()


def render_steps_stage():
    """Render the chosen recipe's ingredient list and numbered cooking steps."""
    steps_data = st.session_state.steps
    st.subheader(steps_data.get("name", "Recipe"))

    st.markdown("**Ingredients needed:**")
    for item in steps_data.get("ingredients_needed", []):
        st.markdown(f"- {item}")

    st.markdown("**Steps:**")
    for i, step in enumerate(steps_data.get("steps", []), start=1):
        st.markdown(f"{i}. {step}")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Back to suggestions"):
            st.session_state.stage = "suggestions"
            st.rerun()
    with col2:
        if st.button("Start over"):
            reset_to_input()
            st.rerun()


def reset_to_input():
    """Clear stored recipe state and send the user back to the input stage."""
    st.session_state.stage = "input"
    st.session_state.suggestions = None
    st.session_state.selected_recipe = None
    st.session_state.steps = None
    st.session_state.chat_history = []


def main():
    """Configure the page, guard against a missing API key, and dispatch to the current stage."""
    st.set_page_config(page_title="MealPlanner AI", page_icon="🍳")
    st.title("🍳 MealPlanner AI")
    st.caption("A smart meal planner for when you don't know what to cook with what you've got.")

    if not get_api_key():
        st.error("GEMINI_API_KEY is not set. Copy .env.example to .env and add your API key.")
        st.stop()

    init_session_state()
    client = build_client()

    if st.session_state.stage == "input":
        render_input_stage(client)
    elif st.session_state.stage == "suggestions":
        render_suggestions_stage(client)
    elif st.session_state.stage == "steps":
        render_steps_stage()

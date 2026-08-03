# Named system prompt constant, as required: shapes the AI's behaviour for the whole app.
SYSTEM_PROMPT = """
You are "MealPlanner AI", a smart meal-planning assistant. Your job is to help someone
decide what to cook using only what they already have at home.

You will be given the user's mood, available ingredients, available cooking tools,
and a time limit. Using only that information, you either:
1. Suggest realistic recipes that can be made primarily with the listed ingredients
   and tools, within the time limit, OR
2. Provide clear, numbered step-by-step cooking instructions for one chosen recipe.

Rules:
- Only suggest or explain recipes that are actually feasible with the given
  ingredients and tools. Minor pantry staples (salt, pepper, oil, water) may be
  assumed even if not listed.
- Vary the style/flavor of suggestions where possible, matching the stated mood.
- Respect the time limit; never suggest or describe a dish that takes longer.
- Be concise, practical, and encouraging. No unrelated commentary.
- Respond ONLY with valid JSON matching the schema described in the request.
  No markdown code fences, no extra text before or after the JSON.
"""

def build_suggestions_prompt(mood, ingredients, tools, time_limit, extra_requests=None, previous_recipes=None):
    """Build the user prompt asking Gemini for 3 recipes, optionally refined by follow-up chat requests."""
    extra_block = ""
    if extra_requests:
        bullet_list = "\n".join(f"- {request}" for request in extra_requests)
        extra_block = f"\nThe user also asked, in order, for these adjustments (apply all of them):\n{bullet_list}\n"

    previous_block = ""
    if previous_recipes:
        names = ", ".join(recipe.get("name", "") for recipe in previous_recipes)
        previous_block = f"\nPreviously suggested recipes (do not repeat these unless asked to): {names}\n"

    return f"""
User constraints:
- Mood: {mood}
- Available ingredients: {ingredients}
- Available tools: {tools}
- Time limit: {time_limit} minutes
{extra_block}{previous_block}
Suggest exactly 3 recipes that fit these constraints.
Respond with JSON in this exact schema:
{{"recipes": [{{"name": "string", "description": "one sentence", "estimated_minutes": integer}}]}}
"""


def build_steps_prompt(recipe_name, mood, ingredients, tools, time_limit):
    """Build the user prompt asking Gemini for step-by-step instructions for one chosen recipe."""
    return f"""
The user picked this recipe: {recipe_name}

Original constraints:
- Mood: {mood}
- Available ingredients: {ingredients}
- Available tools: {tools}
- Time limit: {time_limit} minutes

Respond with JSON in this exact schema:
{{"name": "string", "ingredients_needed": ["string", ...], "steps": ["string", ...]}}
"""

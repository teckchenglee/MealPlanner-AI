# MealPlanner AI

MealPlanner AI is a Streamlit web app that suggests recipes based on your mood, the ingredients and tools you have on hand, and how much time you've got. It's for anyone standing in front of their fridge who doesn't know what to cook with what's already there.

## Problem Statement

Deciding what to cook with limited ingredients, tools, and time is a small but recurring source of friction, and it often ends in food waste or a takeout order. MealPlanner AI removes that friction by turning what you already have into concrete, feasible recipe ideas and step-by-step instructions, so you don't need to search recipes online and hope they match your pantry.

## Technology Stack

Python, Streamlit, google-genai, python-dotenv, Google Gemini API (`gemini-flash-latest`).

## Setup Instructions

1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env` and fill in your Gemini API key:
   ```
   GEMINI_API_KEY="your-api-key-here"
   ```
4. Run the application:
   ```bash
   streamlit run app.py
   ```

## Usage Examples

**Example 1**

- Input: Mood = "something comforting", Ingredients = "eggs, rice, spinach, garlic", Tools = "stovetop", Time limit = 30 minutes
- Output: The app suggests 3 recipes (e.g. "Garlic Spinach Fried Rice", "Soft Scrambled Eggs on Rice", "Spinach & Egg Rice Bowl"), each with a one-sentence description and estimated cook time. Picking one returns a full ingredient list and numbered cooking steps.

**Example 2**

- Input: Mood = "something light and refreshing", Ingredients = "chicken breast, tomato, cucumber, lettuce", Tools = "stovetop, microwave", Time limit = 20 minutes, then a chat refinement of "give me other options"
- Output: The app returns 3 new recipe suggestions that avoid repeating the previous set (e.g. a chicken salad, a stir-fry, a wrap), still fitting the 20-minute limit.

## Known Limitations

- The app trusts the model's JSON output; if Gemini returns malformed JSON or an unexpected schema, the request fails and the user just sees a generic error with no fallback or retry.
- There's no validation of ingredient/tool input or nutritional awareness (allergies, dietary restrictions, calorie goals), so suggestions can be impractical or unsuitable for some users.

## Future Improvements

- Let users specify dietary restrictions and allergies, and have the model respect them in both suggestions and steps.
- Persist favorite recipes and past sessions (e.g. to a local file or database) so users can revisit meals they've cooked before.

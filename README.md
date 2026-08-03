# MealPlanner AI

[![CI](https://github.com/teckchenglee/MealPlanner-AI/actions/workflows/ci.yml/badge.svg)](https://github.com/teckchenglee/MealPlanner-AI/actions/workflows/ci.yml)

MealPlanner AI is a Streamlit web app that suggests recipes based on your mood, the ingredients and tools you have on hand, and how much time you've got. It's for anyone standing in front of their fridge who doesn't know what to cook with what's already there.

## Problem Statement

Many people struggle to decide what to cook using the ingredients, equipment, and time they have available. Existing recipe platforms require users to search through countless recipes, many of which are impractical or require additional ingredients. This often results in decision fatigue, wasted food, and increased reliance on takeout. MealPlanner AI addresses this problem by generating personalized recipes based on the user's available ingredients, kitchen tools, and time constraints, making home cooking simpler, faster, and more sustainable.

## Technology Stack

Python, Streamlit, google-genai, python-dotenv, Google Gemini API (`gemini-flash-latest`).

## Setup Instructions

1. Clone the repository.
2. Create and activate a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate   # on Windows: .venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Copy `.env.example` to `.env` and fill in your Gemini API key:
   ```
   GEMINI_API_KEY="your-api-key-here"
   ```
5. Run the application:
   ```bash
   streamlit run main.py
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

## CI/CD

Every push and pull request to `main` runs the GitHub Actions workflow in `.github/workflows/ci.yml`, which lints the code and verifies all modules import cleanly.

The app is deployed via [Streamlit Community Cloud](https://share.streamlit.io), which auto-redeploys on every push to `main`:

1. Sign in to share.streamlit.io with GitHub.
2. Click "New app", select this repository, branch `main`, and main file `app.py`.
3. Under "Advanced settings" → "Secrets", add:
   ```
   GEMINI_API_KEY = "your-api-key-here"
   ```
4. Deploy. Future pushes to `main` redeploy automatically.

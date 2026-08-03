# MealPlanner AI

[![CI](https://github.com/teckchenglee/MealPlanner-AI/actions/workflows/ci.yml/badge.svg)](https://github.com/teckchenglee/MealPlanner-AI/actions/workflows/ci.yml)

MealPlanner AI is a Streamlit web app that suggests recipes based on your mood, available ingredients, kitchen tools, and available cooking time. Instead of searching through recipes that may not match what you have, the app creates practical meal ideas using the resources already in your kitchen, helping reduce decision fatigue and food waste.

**Live app:** https://mealplanner-ai.streamlit.app/

## Problem Statement

Many people struggle to decide what to cook using the ingredients, equipment, and time they have available. Existing recipe platforms require users to search through countless recipes, many of which are impractical or require additional ingredients. This often results in decision fatigue, wasted food, and increased reliance on takeout. MealPlanner AI addresses this problem by generating personalized recipes based on the user's available ingredients, kitchen tools, and time constraints, making home cooking simpler, faster, and more sustainable.

## Technology Stack

Python, Streamlit, Google Gemini API (`google-genai`), python-dotenv.

**CI/CD**: GitHub Actions (ruff lint + import checks + deployed-app smoke test) and Streamlit Community Cloud (hosting, auto-redeploy on push to `main`).

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

## CI/CD

Every push and pull request to `main` runs the GitHub Actions workflow in `.github/workflows/ci.yml`, which lints the code and verifies all modules import cleanly. On pushes to `main`, a second job then does a smoke check — it curls the live app to confirm it's reachable (Streamlit Community Cloud handles the actual redeploy itself, so this is a health check, not a deploy trigger).

The app is deployed via [Streamlit Community Cloud](https://share.streamlit.io) at **https://mealplanner-ai.streamlit.app/**, which auto-redeploys on every push to `main`:

1. Sign in to share.streamlit.io with GitHub.
2. Click "New app", select this repository, branch `main`, and main file `main.py`.
3. Under "Advanced settings" → "Secrets", add:
   ```
   GEMINI_API_KEY = "your-api-key-here"
   ```
4. Deploy. Future pushes to `main` redeploy automatically.

## Known Limitations

- The app relies on the LLM to return valid JSON. If the response is malformed, a generic error message is displayed without an automatic retry. If the response is valid JSON but missing expected fields (e.g. the `"recipes"` list) the app does not display any suggestions and provides no specific feedback to the user.
- The app does not validate ingredient or kitchen tool inputs, nor does it account for dietary preferences, allergies, nutritional requirements, or calorie goals. As a result, some generated recipes may be impractical or unsuitable for individual users.

## Future Improvements

- Support dietary preferences, allergies, and nutritional goals by allowing users to specify these constraints and ensuring all generated recipe suggestions and cooking instructions adhere to them.
- Add persistent storage for favorite recipes and cooking history (e.g., using a local database or cloud storage), enabling users to revisit, organize, and reuse previously generated meals.

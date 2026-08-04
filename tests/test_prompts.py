from prompts import build_steps_prompt, build_suggestions_prompt


def test_suggestions_prompt_includes_all_constraints():
    prompt = build_suggestions_prompt("cozy", "eggs, rice", "stovetop", 30)
    assert "cozy" in prompt
    assert "eggs, rice" in prompt
    assert "stovetop" in prompt
    assert "30 minutes" in prompt
    assert "adjustments" not in prompt
    assert "Previously suggested" not in prompt


def test_suggestions_prompt_omits_blocks_for_empty_lists():
    prompt = build_suggestions_prompt("cozy", "eggs", "oven", 20, extra_requests=[], previous_recipes=[])
    assert "adjustments" not in prompt
    assert "Previously suggested" not in prompt


def test_suggestions_prompt_includes_extra_requests_in_order():
    prompt = build_suggestions_prompt(
        "cozy", "eggs", "oven", 20,
        extra_requests=["I also have chicken", "make it spicier"],
    )
    assert "- I also have chicken" in prompt
    assert "- make it spicier" in prompt
    assert prompt.index("I also have chicken") < prompt.index("make it spicier")


def test_suggestions_prompt_lists_previous_recipe_names():
    previous = [{"name": "Fried Rice"}, {"name": "Omelette"}]
    prompt = build_suggestions_prompt("cozy", "eggs", "oven", 20, previous_recipes=previous)
    assert "Fried Rice, Omelette" in prompt


def test_suggestions_prompt_tolerates_recipe_missing_name():
    # Edge case: a previous recipe dict without a "name" key shouldn't crash prompt building.
    previous = [{"name": "Fried Rice"}, {"description": "no name field"}]
    prompt = build_suggestions_prompt("cozy", "eggs", "oven", 20, previous_recipes=previous)
    assert "Fried Rice, " in prompt


def test_steps_prompt_includes_recipe_and_constraints():
    prompt = build_steps_prompt("Garlic Fried Rice", "cozy", "eggs, rice, garlic", "stovetop", 25)
    assert "Garlic Fried Rice" in prompt
    assert "cozy" in prompt
    assert "eggs, rice, garlic" in prompt
    assert "stovetop" in prompt
    assert "25 minutes" in prompt

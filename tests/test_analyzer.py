import analyzer


def test_get_recipe_suggestions_returns_recipes_on_success(monkeypatch):
    monkeypatch.setattr(analyzer, "generate_json", lambda client, prompt: '{"recipes": [{"name": "Fried Rice"}]}')
    result = analyzer.get_recipe_suggestions(None, "cozy", "eggs, rice", "stovetop", 30)
    assert result == [{"name": "Fried Rice"}]


def test_get_recipe_suggestions_returns_none_when_recipes_key_missing(monkeypatch):
    # Edge case: valid JSON but the wrong shape. Currently fails silently (no st.error) -
    # this test documents that known limitation so a future fix has to touch this test too.
    errors = []
    monkeypatch.setattr(analyzer, "generate_json", lambda client, prompt: '{"unexpected": true}')
    monkeypatch.setattr(analyzer.st, "error", lambda msg: errors.append(msg))
    result = analyzer.get_recipe_suggestions(None, "cozy", "eggs", "stovetop", 30)
    assert result is None
    assert errors == []


def test_get_recipe_suggestions_returns_none_when_recipes_list_empty(monkeypatch):
    monkeypatch.setattr(analyzer, "generate_json", lambda client, prompt: '{"recipes": []}')
    result = analyzer.get_recipe_suggestions(None, "cozy", "eggs", "stovetop", 30)
    assert result is None


def test_get_recipe_suggestions_shows_error_on_malformed_json(monkeypatch):
    errors = []
    monkeypatch.setattr(analyzer, "generate_json", lambda client, prompt: "not json at all")
    monkeypatch.setattr(analyzer.st, "error", lambda msg: errors.append(msg))
    result = analyzer.get_recipe_suggestions(None, "cozy", "eggs", "stovetop", 30)
    assert result is None
    assert len(errors) == 1
    assert "recipe suggestions" in errors[0]


def test_get_recipe_steps_returns_dict_on_success(monkeypatch):
    monkeypatch.setattr(
        analyzer, "generate_json",
        lambda client, prompt: '{"name": "Fried Rice", "steps": ["Cook rice"]}',
    )
    result = analyzer.get_recipe_steps(None, "Fried Rice", "cozy", "eggs, rice", "stovetop", 30)
    assert result == {"name": "Fried Rice", "steps": ["Cook rice"]}


def test_get_recipe_steps_shows_error_on_malformed_json(monkeypatch):
    errors = []
    monkeypatch.setattr(analyzer, "generate_json", lambda client, prompt: "{broken")
    monkeypatch.setattr(analyzer.st, "error", lambda msg: errors.append(msg))
    result = analyzer.get_recipe_steps(None, "Fried Rice", "cozy", "eggs", "stovetop", 30)
    assert result is None
    assert len(errors) == 1
    assert "recipe steps" in errors[0]

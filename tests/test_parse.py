import json

import pytest

from parse import parse_json_response


def test_parses_plain_json():
    assert parse_json_response('{"recipes": []}') == {"recipes": []}


def test_strips_fenced_json_with_language_tag():
    raw = '```json\n{"recipes": [{"name": "Rice"}]}\n```'
    assert parse_json_response(raw) == {"recipes": [{"name": "Rice"}]}


def test_strips_fenced_json_without_language_tag():
    raw = '```\n{"a": 1}\n```'
    assert parse_json_response(raw) == {"a": 1}


def test_handles_surrounding_whitespace():
    raw = '\n\n  {"a": 1}  \n'
    assert parse_json_response(raw) == {"a": 1}


def test_empty_response_raises_json_decode_error():
    with pytest.raises(json.JSONDecodeError):
        parse_json_response("")


def test_malformed_json_raises_json_decode_error():
    with pytest.raises(json.JSONDecodeError):
        parse_json_response('{"recipes": [')


def test_non_json_prose_raises_json_decode_error():
    with pytest.raises(json.JSONDecodeError):
        parse_json_response("Sorry, I can't help with that.")

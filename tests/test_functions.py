"""
Tests for ArmThingyFunctions
"""


def test_flatten():
    """Test the flatten function with various inputs."""
    from ArmThingyFunctions import flatten
    d0 = {}
    assert flatten(d0) == {}

    d1 = {"a": "1", "b": {"c": "2"}}
    assert flatten(d1) == {"a": "1", "c": "2"}

    d2 = {"x": {"y": "3", "z": "4"}, "w": "5"}
    assert flatten(d2) == {"y": "3", "z": "4", "w": "5"}

    d3 = {"p": {"q": {"r": "6"}}}
    assert flatten(d3) == {"r": "6"}

    d4 = {"m": {"n": {"o": {"p": "7"}}}}
    assert flatten(d4) == {"p": "7"}


def test_pretty_time_delta():
    """Test the pretty_time_delta function with various inputs."""
    from ArmThingyFunctions import pretty_time_delta
    from datetime import timedelta
    assert pretty_time_delta(timedelta(seconds=0)) == "0s"
    assert pretty_time_delta(timedelta(seconds=1)) == "1s"
    assert pretty_time_delta(timedelta(minutes=1)) == "1m 0s"
    assert pretty_time_delta(timedelta(hours=1)) == "1h 0s"
    assert pretty_time_delta(timedelta(days=1)) == "1d 0s"


def test_snake_case_to_human_case():
    """Test the snake_case_to_human_case function with various inputs."""
    from ArmThingyFunctions import snake_case_to_human_case
    assert snake_case_to_human_case('') == ''
    assert snake_case_to_human_case('snake_case') == 'Snake Case'
    assert snake_case_to_human_case('notSnakeCase') == 'Notsnakecase'
    assert snake_case_to_human_case('with_numbers_123') == 'With Numbers 123'
    assert snake_case_to_human_case('with_numbers_123_four_five') == 'With Numbers 123 Four Five'
    assert snake_case_to_human_case('with_http_acronym') == 'With Http Acronym'
    assert snake_case_to_human_case('id_should_be_uppercase') == 'ID Should Be Uppercase'


def test_camel_case_to_snake_case():
    """Test the camel_case_to_snake_case function with various inputs."""
    from ArmThingyFunctions import camel_case_to_snake_case
    assert camel_case_to_snake_case('') == ''
    assert camel_case_to_snake_case('hello') == 'hello'
    assert camel_case_to_snake_case('CamelCase') == 'camel_case'
    assert camel_case_to_snake_case('withNumbers123') == 'with_numbers_123'
    assert camel_case_to_snake_case('withNumbers123FourFive') == 'with_numbers_123_four_five'
    assert camel_case_to_snake_case('withHTTPAcronym') == 'with_http_acronym'
    assert camel_case_to_snake_case('IDShouldBeIntact') == 'id_should_be_intact'

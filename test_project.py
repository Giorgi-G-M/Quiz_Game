import pytest
from project import add_new_user, update_score_and_difficulty, get_user_data, get_timer_duration, next_difficulty, format_choices

# Test add_new_user function
def test_add_new_user():
    assert add_new_user('Alice', 'Smith', 'AS') == True

# Test update_score_and_difficulty function
def test_update_score_and_difficulty():
    updated = update_score_and_difficulty('Alice', 'Smith', 'AS', 60, 'Medium')
    assert updated == True
    user_data = get_user_data('Alice', 'Smith', 'AS')
    assert user_data == {'Name': 'Alice', 'Surname': 'Smith', 'Nickname': 'AS', 'Score': '60', 'Difficulty': 'Medium'}

def test_next_difficulty():
    assert next_difficulty('Easy') == 'Medium'

# Test cases for format_choices function
def test_format_choices():
    assert format_choices(['A', 'B', 'C']) == ['A', 'B', 'C']
    assert format_choices([]) == ['No choices available']

# Test cases for get_timer_duration function
def test_get_timer_duration():
    assert get_timer_duration('Easy') == 120
    assert get_timer_duration('Medium') == 180


import pytest

@pytest.fixture
def line_normal_scenario():
    return {
        'line': "allocation, -Float-, (what percentage of loan is payed by payment)",
        'help_text': 'what percentage of loan is payed by payment',
        'field_type': 'Float'
    }

@pytest.fixture
def line_mini_scenario():
    return {
        'line': "allocation",
        'help_text': '',
        'field_type': 'Char'
    }

@pytest.fixture
def line_help_scenario():
    return {
        'line': "allocation, (what percentage of loan is payed by payment)",
        'help_text': 'what percentage of loan is payed by payment',
        'field_type': 'Char'
    }
import pytest
import re

from utils.field_handlers import get_help_text, get_field_type, process_field_line


def test_get_help_text(line_normal_scenario):
    help_text = get_help_text(line_normal_scenario['line'])
    assert help_text == line_normal_scenario['help_text']

def test_get_field_type(line_normal_scenario):
    field_type = get_field_type(line_normal_scenario['line'])
    assert field_type == line_normal_scenario['field_type']

def test_process_field_line(line_normal_scenario):
    resp = process_field_line(line_normal_scenario['line'])
    assert re.match(r'allocation = models.FloatField.+', resp)

def test_incomplete_line(line_mini_scenario, line_help_scenario):
    resp = process_field_line(line_mini_scenario['line'])
    assert re.match(r'allocation = models.CharField.+', resp)
    resp = process_field_line(line_help_scenario['line'])
    assert re.match(r'allocation = models.CharField.+', resp)
    assert line_help_scenario['help_text'] in resp

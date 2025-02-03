"""Tests that cover functionality in scripts/local_cli.py."""

import random

import pytest

from format_xml.format_xml import sort_and_format_xml


@pytest.mark.general
def test_sort_and_format_drawio_xml() -> None:
    """Test that covers sort_and_format_xml() in format_xml.py with .drawio XML file content."""
    xml_string = """<example body="one" content="two" attribute="three">Hello</example>"""
    formatted_xml = sort_and_format_xml(xml_string)
    assert formatted_xml == '<example attribute="three" body="one" content="two">Hello</example>'

    mx_cell_attributes = [
        'id="cS6q8hUBTjx84kLF-eMw-11"',
        'parent="1"',
        'style="rounded=1;whiteSpace=wrap;html=1;fillColor=#d80073;fontColor=#ffffff;strokeColor=#A50040;"',
        'value="how do we know that these inspections are getting tracked / monitored / missed?"',
        'vertex="1"',
    ]
    mx_geometry_attributes = [
        'as="geometry"',
        'height="60"',
        'width="120"',
        'x="450"',
        'y="260"',
    ]
    # Shuffle attributes within <mxCell> and <mxGeometry> and assert sorting returns same output.
    expected_formatted_xml = "".join(
        [
            '<mxCell id="cS6q8hUBTjx84kLF-eMw-11" parent="1" ',
            'style="rounded=1;whiteSpace=wrap;html=1;fillColor=#d80073;fontColor=#ffffff;strokeColor=#A50040;" ',
            'value="how do we know that these inspections are getting tracked / monitored / missed?" vertex="1">',
            '<mxGeometry as="geometry" height="60" width="120" x="450" y="260"/></mxCell>',
        ]
    )
    for _ in range(10):
        random.shuffle(mx_cell_attributes)
        random.shuffle(mx_geometry_attributes)
        unformatted_xml = "".join(
            [f"<mxCell {' '.join(mx_cell_attributes)}><mxGeometry {' '.join(mx_geometry_attributes)}/></mxCell>"]
        )
        # Ensure that unformatted XML is not the expected XML before applying sorting. It is extremely unlikely for this
        # to fail, with 1/10! odds (1 in 3,628,800) of the shuffled attributes matching the sorted attributes.
        assert unformatted_xml != expected_formatted_xml
        actual_formatted_xml = sort_and_format_xml(unformatted_xml)
        assert actual_formatted_xml == expected_formatted_xml

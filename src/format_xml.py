"""Format .drawio XML file content: sort attributes within XML elements alphabetically and pretty-print content."""

import os
import xml.etree.ElementTree as ET
from xml.dom import minidom


def run_command(command: str, display_command: str = "") -> None:
    """Simple wrapper for running terminal command.

    Args:
        command (str): Command to run in terminal.
        display_command (str, optional): What to display to terminal as the command run (defaults to 'command').

    Returns:
        None: command executed as if it were run in the terminal.
    """
    if not display_command:
        display_command = command
    print(display_command)
    os.system(command)


def sort_attributes(element: ET.Element) -> None:
    """Sort the attributes of each element in alphabetical order and update the element's attributes, also recursively
    applies sort_attributes() to child elements.

    Args:
        element (ET.Element): Current XML Element, either root of whole tree or any branch.
    """
    # Sort the attributes of the element alphabetically
    sorted_attrib = dict(sorted(element.attrib.items()))
    element.attrib.clear()
    element.attrib.update(sorted_attrib)

    # Recursively sort attributes for all child elements
    for child in element:
        sort_attributes(child)


def sort_and_format_xml(xml_string: str) -> str:
    """Format XML file content with sorted inner attributes and pretty-printing.

    Args:
        xml_string (str): Initial XML file content.

    Raises:
        ElementTree.ParseError: Thrown if malformed XML string content passed in.

    Returns:
        str: Output XML file content with sorted inner attributes and pretty-printing.
    """
    try:
        root = ET.fromstring(xml_string)
    except ET.ParseError as parse_error:
        raise parse_error

    # Recursively sort inner attributes of XML elements.
    sort_attributes(root)

    xml_bytestring = ET.tostring(root, "utf-8")
    reparsed = minidom.parseString(xml_bytestring)
    xml_string = reparsed.toprettyxml(indent="", newl="")
    xml_string = xml_string.replace('<?xml version="1.0" ?>', "")
    return xml_string


def get_drawio_filenames() -> list[str]:
    """Return list of .drawio files with relative paths,
    i.e. "./docs-public/specifications/images/signals/signals.drawio".

    Returns:
        list[str]: List of relative paths to .drawio files.
    """
    filenames = []
    for root, dirs, files in os.walk(".", topdown=True):  # pylint: disable=unused-variable
        for filename in files:
            if filename.endswith(".drawio"):
                filenames.append(os.path.join(root, filename))
    return filenames


def main() -> None:
    """Format all .drawio files with js-beautify HTML formatter and config as well sort inner attributes.

    Raises:
        ElementTree.ParseError: Thrown if malformed XML content detected in one of the .drawio files.
    """
    filenames = get_drawio_filenames()
    for filename in filenames:
        with open(filename, "r", encoding="utf-8") as original_drawio_file:
            drawio_content = original_drawio_file.read()
        try:
            formatted_xml = sort_and_format_xml(drawio_content)
        except ET.ParseError as parse_error:
            print(f"ERROR with filename '{filename}'")
            raise parse_error
        with open(filename, "w", encoding="utf-8") as original_drawio_file:
            original_drawio_file.write(formatted_xml)

        run_command(
            " ".join(
                [
                    f'node node_modules/js-beautify/js/lib/cli.js -f "{filename}"',
                    "--type=html --replace --config=js-beautify.json",
                ]
            )
        )


if __name__ == "__main__":
    main()

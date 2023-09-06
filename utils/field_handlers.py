"""
The code provided is a Python script that processes a 
field line and generates a corresponding Django model field code. 

Here is a breakdown of the code:

- The regular expression  `help_text_reg`  is defined to match the help text within parentheses in a field line.
- The regular expression  `field_type_reg`  is defined to match the field type within hyphens in a field line.


Overall, the code provides a way to process field lines and 
generate Django model field codes based on the field type 
and help text present in the lines.
"""
import re

help_text_reg = re.compile(r".+\((?P<help_text>.+)\).*")
field_type_reg = re.compile(r".+-(?P<field_type>.+)-.*")


def process_field_line(line: str) -> str:
    """
    takes a field line as input and returns the generated
    Django model field code. It determines the field type
    using the  `get_field_type()`  function and selects
    the appropriate handler function from the  `field_handlers`
    dictionary. If no field type is found, it defaults to 'Char'.
    The handler function is then called to generate the code,
    using the  `get_help_text()`  and  `get_field_name()`
    functions to extract the help text and field name from the line.
    """
    field_handlers = {
        "Char": char_field_handler,
        "Decimal": decimal_field_handler,
        "Foreign": foreign_field_handler,
        "File": file_field_handler,
    }
    field_type = get_field_type(line)
    if not field_type:
        field_type = "Char"
    handler = field_handlers.get(field_type, default_field_handler)
    code = handler(line)
    name = get_field_name(line)
    return f"{name} = models.{code}"


def get_field_name(line: str) -> str:
    """
    extracts the field name from the line,
    considering the possibility of a comma-separated format.
    """
    if "," in line:
        return line.strip().split(",")[0]
    else:
        return line


def get_help_text(line: str) -> str:
    """
    uses the  `help_text_reg`  regular
    expression to extract the help text from the line.
    """
    found = help_text_reg.search(line)
    return found.group("help_text") if found else ""


def get_field_type(line: str) -> str:
    """
    uses the  `field_type_reg`  regular expression to extract the field type from the line.
    """
    found = field_type_reg.search(line)
    return found.group("field_type") if found else ""


def char_field_handler(line: str) -> str:
    """
    handler function for specific field types.
    They use the extracted help text to generate
    the corresponding Django model field code.
    """
    help_text = get_help_text(line)
    return f'CharField(max_length=100, help_text="{help_text}")'


def decimal_field_handler(line: str) -> str:
    """
    handler function for specific field types.
    They use the extracted help text to generate
    the corresponding Django model field code.
    """
    help_text = get_help_text(line)
    return f'DecimalField(max_digits=45, decimal_places=35, help_text="{help_text}")'


def foreign_field_handler(line: str) -> str:
    """
    handler function for specific field types.
    They use the extracted help text to generate
    the corresponding Django model field code.
    """
    help_text = get_help_text(line)
    return f'ForeignKey("", on_delete=models.CASCADE, help_text="{help_text}")'


def file_field_handler(line: str) -> str:
    """
    handler function for specific field types.
    They use the extracted help text to generate
    the corresponding Django model field code.
    """
    help_text = get_help_text(line)
    return f'FileField(upload_to="files", help_text="{help_text}")'


def default_field_handler(line: str) -> str:
    """
    fallback handler that is used when the
    field type is not recognized. It generates a
    generic field code using the extracted
    field type and help text.
    """
    field_type = get_field_type(line)
    help_text = get_help_text(line)
    return f'{field_type}Field(help_text="{help_text}")'

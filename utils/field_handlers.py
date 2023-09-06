import re

help_text_reg = re.compile(r'.+\((?P<help_text>.+)\).*')
field_type_reg = re.compile(r'.+-(?P<field_type>.+)-.*')

def process_field_line(line:str)->str:
    field_handlers = {
        'Char': char_field_handler,
        'Decimal': decimal_field_handler,
        'Foreign': foreign_field_handler,
        'File': file_field_handler,
    }
    field_type = get_field_type(line)
    if not field_type:
        field_type = 'Char'
    handler = field_handlers.get(field_type, default_field_handler)
    code = handler(line)
    name = get_field_name(line)
    return f'{name} = models.{code}'

def get_field_name(line:str)->str:
    if ',' in line:
        return line.strip().split(',')[0]
    else:
        return line

def get_help_text(line:str)->str:
    found = help_text_reg.search(line)
    return found.group('help_text') if found else ""

def get_field_type(line:str)->str:
    found = field_type_reg.search(line)
    return found.group('field_type') if found else ""

def char_field_handler(line:str)->str:
    help_text = get_help_text(line)
    return f'CharField(max_length=100, help_text="{help_text}")'

def decimal_field_handler(line:str)->str:
    help_text = get_help_text(line)
    return f'DecimalField(max_digits=45, decimal_places=35, help_text="{help_text}")'

def foreign_field_handler(line:str)->str:
    help_text = get_help_text(line)
    return f'ForeignKey("", on_delete=models.CASCADE, help_text="{help_text}")'

def file_field_handler(line:str)->str:
    help_text = get_help_text(line)
    return f'FileField(upload_to="files", help_text="{help_text}")'

def default_field_handler(line:str)->str:
    field_type = get_field_type(line)
    help_text = get_help_text(line)
    return f'{field_type}Field(help_text="{help_text}")'
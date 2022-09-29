import pandas as pd
from pathlib import Path
from utility.exceptions import ValidationError
from utility.constants import answer_type_strings_to_key

def get_columns(filename:str, extension:str):
    file_path = Path.cwd()/f'file_upload_folder/{filename}.{extension}'
    if extension=='csv':
        data = pd.read_csv(file_path)
        return list(data.columns)
    elif extension=='xlsx':
        data = pd.read_excel(file_path)
        return list(data.columns)
    else:
        raise ValidationError('Uploaded file appears to be corrupted.')


def get_file_data(file_id:str, extension:str):
    file_path = Path.cwd()/f'file_upload_folder/{file_id}.{extension}'
    if extension=='csv':
        return pd.read_csv(file_path)
    elif extension=='xlsx':
        return pd.read_excel(file_path)
    else:
        raise ValidationError('Uploaded file appears to be corrupted.')


def get_answer_type_key_list_from_string_value(answer_type:list):
    return [answer_type_strings_to_key[v.strip()] for v in answer_type]

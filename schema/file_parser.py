from pydantic import BaseModel

class Field(BaseModel):
    file_column_in_source:str|None=None
    file_column_in_target:str
    default_value:str|None=None

class FileFields(BaseModel):
    extension:str #choice b/w csv or xlsx
    file_id:str
    fields:list[Field]
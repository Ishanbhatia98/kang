from fastapi.routing import APIRouter
from fastapi import status, UploadFile
from utility.exceptions import ValidationError
from pydantic import BaseModel
from pathlib import Path
from kang.custom_logger import GetLogger
from utility.file_parser import get_columns, get_file_data, get_answer_type_key_list_from_string_value
from secrets import token_hex
from utility.constants import required_fields
from domains.org_template_evaluation import OrgTemplateEvaluationService
from domains.org_template_evaluation_criteria import OrgTemplateEvaluationCriteriaService
from domains.org_template_evaluation_requirement import OrgTemplateEvaluationRequirementService
from domains.org_template_evaluation_requirement_options import OrgTemplateEvaluationRequirementOptionsService
from collections import defaultdict 

logger = GetLogger(__name__)
router = APIRouter(prefix='/web/v0', tags=['FILE-PARSER'])

@router.post('/upload-file/', status_code=status.HTTP_201_CREATED)
def upload_file(file: UploadFile):
    #csv/xlsx file
    #store in temporary folder
    #generate file_id for the uploaded file
    #parse file and return column names
    file_id = token_hex(7).lower()
    filename = file.filename
    if '.' not in filename:
        raise ValidationError('Please upload a csv/xlsx file only')

    file_extension = filename.split('.')[-1]
    if file_extension not in ['csv', 'xlsx']:
        raise ValidationError('Please upload a csv/xlsx file only')
    try:
        contents = file.file.read()
        with open(Path.cwd()/f'file_upload_folder/{file_id}.{file_extension}', 'wb') as f:
            f.write(contents)
    except Exception as e:
        logger.info(msg="There was an error uploading the file")
        raise ValidationError('File could not be uploaded...') from e
    file_columns = get_columns(file_id, file_extension)
    return {
        "message": f"Successfully uploaded {file.filename}",
        "file_id": file_id,
        "extension": file_extension,
        "column_names": file_columns
    }


class Field(BaseModel):
    file_column_in_source:str
    file_column_in_target:str
    default_value:str|None=None

class FileFields(BaseModel):
    extension:str #choice b/w csv or xlsx
    file_id:str
    fields:list[Field]

@router.post('/validate-fields/', status_code=status.HTTP_200_OK)
def parse_and_validate_file_fields(file_fields:FileFields):
    file_id = file_fields.file_id
    fields = file_fields.fields
    source_fields, target_fields = [], []
    target_source_field_map = defaultdict(lambda:None)

    #validating fields, mandatory fields
    for i in range(len(fields)):
        source_field, target_field = fields[i].file_column_in_source, fields[i].file_column_in_target
        default_value = fields[i].default_value
        if target_field in required_fields and source_field is None and default_value is None :
            raise ValidationError(f'{target_field} is a required field, please provide a default value')

        source_fields.append(source_field or f'default:{default_value}')
        target_fields.append(target_field)
        target_source_field_map[target_field] = source_field
    
    #getting data as a pandas df
    file_data = get_file_data(file_fields.file_id, file_fields.extension)
    number_of_entries = file_data.shape[0] 
    
    #saving data in tables
    #org_template_evaluation_target_fields = ['template_name'] 
    # #ote
    if 'default:' not in target_source_field_map['template_name']:
        template_name = list(file_data[target_source_field_map['template_name']])
    else:
        default_value = target_source_field_map['template_name'].split(':')[1]
        template_name = [default_value for _ in range(number_of_entries)] 
    OrgTemplateEvaluationService().add_file_entries(
        file_id,
        template_name=template_name
    )


    #org_template_evaluation_criteria_target_fields = ['criteria_name', 'criteria_priority'] 
    # #otec
    if 'default:' not in target_source_field_map['criteria_name']:
        criteria_name = list(file_data[target_source_field_map['criteria_name']])
    else:
        default_value = target_source_field_map['criteria_name'].split(':')[1]
        criteria_name = [default_value for _ in range(number_of_entries)] 

    #optional
    if target_source_field_map['criteria_priority'] and 'default:' not in target_source_field_map['criteria_priority']:
        criteria_priority = list(file_data[target_source_field_map['criteria_priority']])
    elif target_source_field_map['criteria_priority']:
        default_value = target_source_field_map['criteria_priority'].split(':')[1]
        criteria_priority = [default_value for _ in range(number_of_entries)] 
    else:
        criteria_priority = [None for _ in range(number_of_entries)]
    
    OrgTemplateEvaluationCriteriaService().add_file_entries(
        file_id=file_id,
        criteria_name=criteria_name,
        priority=criteria_priority
    )

    # org_template_evaluation_requirement_target_fields = [
    #     'requirement_name', 
    #     'requirement_description',
    #     'requirement_priority',
    #     'answer_type'
    # ] 
    #oter
    if 'default:' not in target_source_field_map['requirement_name']:
        requirement_name = list(file_data[target_source_field_map['requirement_name']])
    else:
        default_value = target_source_field_map['requirement_name'].split(':')[1]
        requirement_name = [default_value for _ in range(number_of_entries)] 

    if 'default:' not in target_source_field_map['requirement_description']:
        requirement_description = list(file_data[target_source_field_map['requirement_description']])
    else:
        default_value = target_source_field_map['requirement_description'].split(':')[1]
        requirement_description = [default_value for _ in range(number_of_entries)] 
    
    #optional
    if  target_source_field_map['requirement_priority'] and 'default:' not in target_source_field_map['requirement_priority']:
        requirement_priority = list(file_data[target_source_field_map['requirement_priority']])
    elif  target_source_field_map['requirement_priority']:
        default_value = target_source_field_map['requirement_priority'].split(':')[1]
        requirement_priority = [default_value for _ in range(number_of_entries)] 
    else:
        requirement_priority = [None for _ in range(number_of_entries)]

    if 'default:' not in target_source_field_map['answer_type']:
        answer_type = list(file_data[target_source_field_map['answer_type']])

    else:
        default_value = target_source_field_map['answer_type'].split(':')[1]
        answer_type = [default_value for _ in range(number_of_entries)] 

    answer_type = get_answer_type_key_list_from_string_value(answer_type)

    OrgTemplateEvaluationRequirementService().add_file_entries(
        file_id=file_id,
        requirement_name=requirement_name,
        requirement_description=requirement_description,
        requirement_priority=requirement_priority,
        answer_type=answer_type
    )

    
    #org_template_evaluation_requirement_options_target_fields = ['requirement_options'] 
    # #otero
    if target_source_field_map['requirement_options'] and 'default:' not in target_source_field_map['requirement_options']:
        requirement_options = list(file_data[target_source_field_map['requirement_options']])
    elif target_source_field_map['requirement_options']:
        default_value = target_source_field_map['requirement_options'].split(':')[1]
        requirement_options = [default_value for _ in range(number_of_entries)] 
    else:
        requirement_options = [None for _ in range(number_of_entries)]
    

    #edit
    option_description = ['default' for _ in range(number_of_entries)]
    OrgTemplateEvaluationRequirementOptionsService().add_file_entries(
        file_id=file_id,
        requiremet_options=requirement_options,
        description =  option_description,
    )


    return {
        'message':'data saved succesfully',
        'file_id':file_id,
        'number_of_entries':number_of_entries
    }
    
    

    



    

    


    




    


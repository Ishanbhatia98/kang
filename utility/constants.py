required_fields  = [
        'template_name',
        'criteria_name',
        'requirement_name',
        'requirement_description',
        'answer_type'
        ]
        
non_required_fields = [
        'requirement_options', 
        'requirement_priority', 
        'criteria_priority'
    ]

answer_type_strings_to_key = {
        'Text':0, #added
        'Rich Text':0,
        'Single Select':1,
        'Multi Select':2,
        'Binary':3,
        'Score':4,
        'File Upload':5,
        'Simple Text':6,
        'Email':7,
        'Phone':8,
        'URL':9,
        'Date':10,
        'Number':11,
        'Currency':12,
        'Radio':13,
        'Checkbox':14
    }
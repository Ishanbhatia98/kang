from kang.base_domain_sql import BaseModelService
from kang.database import Base, mysqldb
from sqlalchemy import String, Column, Integer, Text, Boolean


'''
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `criteria_id` int(10) unsigned DEFAULT NULL,
  `requirement_id` int(10) unsigned DEFAULT NULL,
  `name` varchar(255) NOT NULL,
  `description` text NOT NULL,
  `priority` int(10) unsigned DEFAULT NULL,
  `character_limit` int(10) unsigned DEFAULT NULL,
  `answer_type` int(10) unsigned DEFAULT '1',
  `is_editable` tinyint(1) DEFAULT NULL,
  `is_mandatory` tinyint(1) DEFAULT NULL,
  `seq` int(10) unsigned DEFAULT NULL,
  `is_other_option` tinyint(1) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,

'''

class OrgTemplateEvaluationRequirement(Base):
    __tablename__ = 'org_template_evaluation_requirement'

    file_id = Column(String(150), nullable=False)
    
    id = Column(Integer, primary_key=True, index=True, unique=True)
    criteria_id = Column(Integer, default=None)
    requirement_id = Column(Integer, default=None)
    name = Column(String(255), nullable=True)
    description = Column(Text, nullable=False)
    priority = Column(Integer, default=None)
    character_limit = Column(Integer, default=None)
    answer_type = Column(Integer, default=1) #check
    is_editable = Column(Boolean, default=None) #check
    is_mandatory = Column(Boolean, default=None) #check
    seq = Column(Integer, default=None)
    is_other_option = Column(Boolean, default=None) #check

class OrgTemplateEvaluationRequirementService(BaseModelService):
    
    def __init__(self):
        self.db = mysqldb
        self.model = OrgTemplateEvaluationRequirement
        self.keys = list(self.model.__dict__.keys())
    
    def add_file_entries(
        self,
        file_id:str, 
        requirement_name:list, 
        requirement_description:list, 
        answer_type:list, 
        requirement_priority:list|None
      ):
      number_of_entries = len(requirement_name)
      for i in range(number_of_entries):
        self.create(
          file_id = file_id,
          name = requirement_name[i],
          description=requirement_description[i],
          answer_type = answer_type[i],
          priority =requirement_priority[i] if requirement_priority else None
          )

from email.policy import default
from kang.base_domain_sql import BaseModelService
from kang.database import Base, mysqldb
from sqlalchemy import String, Column, Integer, Text

'''
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `requirement_id` int(10) unsigned DEFAULT NULL,
  `title` varchar(255) DEFAULT NULL,
  `description` text NOT NULL,
  `sequence` int(10) unsigned DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
'''

class OrgTemplateEvaluationRequirementOptions(Base):
    __tablename__ = "org_template_evaluation_requirement_options"
    
    file_id = Column(String(150), nullable=False)

    id = Column(Integer, primary_key=True, index=True, unique=True)
    requirement_id = Column(Integer, default=None)
    title = Column(String(255), default=None)
    description = Column(Text, nullable=False)
    sequence = Column(Integer, default=None)

class OrgTemplateEvaluationRequirementOptionsService(BaseModelService):
  
    def __init__(self):
        self.db = mysqldb
        self.model = OrgTemplateEvaluationRequirementOptions
        self.keys = list(self.model.__dict__.keys())
    
    def add_file_entries(self, file_id:str, requiremet_options:list, description:list):
      number_of_entries = len(requiremet_options)
      for i in range(number_of_entries):
        self.create(
          file_id=file_id,
          title = requiremet_options[i],
          description=description[i]
        )


from kang.base_domain_sql import BaseModelService
from kang.database import Base, mysqldb
from sqlalchemy import String, Column, Integer

'''
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `max_score` int(10) unsigned DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
'''


class OrgTemplateEvaluation(Base):
    __tablename__ = "org_template_evaluation"

    file_id = Column(String(150), nullable=False)

    id = Column(Integer, primary_key=True, index=True, unique=True)
    name = Column(String(255), nullable=False)
    max_score = Column(Integer, default=None)




class OrgTemplateEvaluationService(BaseModelService):
  
    def __init__(self):
        self.db = mysqldb
        self.model = OrgTemplateEvaluation
        self.table_keys = list(self.model.__dict__.keys())
    
    def add_file_entries(self, file_id:str, template_name:list):
      number_of_entries = len(template_name)
      for i in range(number_of_entries):
        self.create(
          file_id = file_id,
          name = template_name[i]
        )
        
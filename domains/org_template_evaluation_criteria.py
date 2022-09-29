from kang.base_domain_sql import BaseModelService
from kang.database import Base, mysqldb
from sqlalchemy import String, Column, Integer, Boolean, Numeric


'''
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `template_id` int(10) unsigned DEFAULT NULL,
  `criteria_id` int(10) unsigned DEFAULT NULL,
  `name` varchar(255) NOT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `is_editable` tinyint(1) DEFAULT '1',
  `is_mandatory` tinyint(1) DEFAULT '0',
  `seq` int(10) unsigned DEFAULT NULL,
  `priority` decimal(10,2) DEFAULT NULL,
'''


#created_at, updated_at check
class OrgTemplateEvaluationCriteria(Base):
    __tablename__ = "org_template_evaluation_criteria"

    file_id = Column(String(150), nullable=False)
    
    id = Column(Integer, primary_key=True, index=True, unique=True)
    template_id = Column(Integer, default=None)
    criteria_id = Column(Integer, default=None)
    name = Column(String(255), nullable=False)
    is_editable = Column(Boolean, default=True) #check
    is_mandatory = Column(Boolean, default=False) #check
    seq = Column(Integer, default=None)
    priority = Column(Numeric(10,2), default=None)


class OrgTemplateEvaluationCriteriaService(BaseModelService):
  
    def __init__(self):
        self.db = mysqldb
        self.model = OrgTemplateEvaluationCriteria
        self.table_keys = list(self.model.__dict__.keys())
    

    def add_file_entries(self, file_id:str, criteria_name:list, priority:list|None):
      number_of_entries = len(criteria_name)
      for i in range(number_of_entries):
        self.create(
          file_id=file_id,
          name=criteria_name[i],
          priority = priority[i] if priority else None
        )
      


      
        
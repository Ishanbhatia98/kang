from datetime import datetime
from sqlalchemy.sql.expression import text
from sqlalchemy import Column,DateTime
from sqlalchemy.ext.declarative import declared_attr
from utility.exceptions import FilterKeyNotPresent, ValidationError, MultipleRecordFoundError

class Base(object):

    @declared_attr
    def __tablename__(self):
        return self.__name__.lower()
    
    created_at = Column(DateTime,default=datetime.now)
    updated_at = Column(DateTime,default=datetime.now,onupdate=datetime.now)

class BaseModelService:
    
    def get_by_id(self,id):
        try:
            return self.db.query(self.model).where(self.model.id==id).first()
        except Exception:
            self.db.rollback()

    #   Filter only direct mapping not >,< only = allowed
    def filter(self,**kwargs):
        keys = kwargs.keys()
        queryset = None
        if not keys:
            raise FilterKeyNotPresent("Filters can not be empty.")

        for key in keys:
            if key not in self.table_keys:
                raise FilterKeyNotPresent(message=f"{key} is not a valid key to filter.")

        try:
            queryset = self.db.query(self.model).filter_by(**kwargs)
            queryset.first() # Just to make sure that the query is valid.
        except Exception as e:
            self.db.rollback()

        return queryset    

    def get_all(self):
        queryset = None
        try:
            queryset = self.db.query(self.model).all()
        except Exception as e:
            self.db.close()

        # def first(self):
        #     if queryset and len(queryset) > 0:
        #         return queryset[0]

        return queryset
    
    def raw_query(self,statement):
        queryset = None
        try:
            queryset = self.db.query(self.model).from_statement(text(statement))
            queryset.count()  # Just to make sure that the query is valid.
        except Exception:
            self.db.rollback()
        return queryset
    

    def create(self,**kwargs):
        model_obj = self.model()
        keys = kwargs.keys()
        try:
            for key in keys:
                exec("model_obj.{0} = kwargs['{0}']".format(key))
        except Exception as e:
            raise ValidationError("Invalid key mapping found while updating database") from e

        self.db.add(model_obj) #Adding record to db with savepoint
        # try:
        if True:
            self.db.commit() # Making data permanent in the db, Error can come here.
        # except Exception as e:
        #     self.db.rollback()
        #     raise ValidationError(e) from e
        return model_obj

    def update(self,model_object,**new_data):
        keys = new_data.keys() # new_data in your case is filenames
        for key in keys:
            exec("model_object.{0} = new_data['{0}']".format(key))
        try:
            self.db.commit() # Making data permanent in the db, Error can come here.
        except Exception as e:
            self.db.rollback()
            raise ValidationError(e) from e
        return model_object
    
    #sql raw race condition
    def update_or_create(self, defaults=None, new_values=None):
        if defaults is None:
            defaults = {}
        if new_values is None:
            new_values = {}
        try:
            existing_queryset = self.filter(**defaults)
            count = existing_queryset.count()
            if count > 1:
                raise MultipleRecordFoundError()

            if count == 0:
                return self.create(**new_values)
            else:
                return self.update(existing_queryset.first(),**new_values)
        except Exception as e:
            self.db.rollback()
            raise ValidationError(e) from e

    def get_or_create(self, defaults=None, new_values=None):
        if defaults is None:
            defaults = {}
        if new_values is None:
            new_values = {}
        try:
            existing_queryset = self.filter(**defaults)
            count = existing_queryset.count()
            if count > 1:
                raise MultipleRecordFoundError()

            return self.create(**new_values) if count == 0 else existing_queryset.first()
        except Exception as e:
            self.db.rollback()
            raise ValidationError(e) from e

    def delete_by_filter(self,**kwargs):
        keys = kwargs.keys()
        if not keys:
            raise FilterKeyNotPresent("Filters can not be empty.")

        for key in keys:
            if key not in self.table_keys:
                raise FilterKeyNotPresent(message=f"{key} is not a valid key to filter.")

        count = self.filter(**kwargs).delete()
        try:
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise ValidationError(e) from e
        return count

    def delete_all(self):
        # This will delete all the record at once.
        count = self.db.query(self.model).delete()
        try:
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise ValidationError(e) from e
        return count

    def get(self, defaults=None):
        if defaults is None:
            defaults = {}
        existing_queryset = self.filter(**defaults)
        count = existing_queryset.count()
        if count > 1:
            raise MultipleRecordFoundError()
        return existing_queryset.first()
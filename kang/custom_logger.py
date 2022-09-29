import logging
import traceback
import json_log_formatter
import sys


class GetLogger():
    def __set_json_logger_formatter(self):
        formatter = json_log_formatter.JSONFormatter()
        json_handler = logging.StreamHandler()
        json_handler.setFormatter(formatter)
        self.internal_logger.addHandler(json_handler)
        self.internal_logger.setLevel(logging.INFO)

    def __init__(self,app_name,formatter="json",set_error_traceback=True):
        self.app_name=app_name
        self.set_error_traceback = set_error_traceback
        self.internal_logger = logging.getLogger(self.app_name)
        if formatter == "json":
            self.__set_json_logger_formatter()
    
    def info(self,msg,*args,**kwargs):
        return self.internal_logger.info(msg,*args,**kwargs)

    def error(self,msg,*args,**kwargs):
        if self.set_error_traceback:
            traceback_error = " ".join(traceback.format_tb(sys.exc_info()[2])).split("\n")
            error_summary = sys.exc_info()[0].__doc__
            extra = kwargs.get("extra",{})
            extra.update(dict(error_summary=error_summary,traceback_error=traceback_error))
            kwargs["extra"] = extra
        return self.internal_logger.error(msg,*args,**kwargs)
    
    def warning(self,msg,*args,**kwargs):
        return self.internal_logger.warning(msg,*args,**kwargs)

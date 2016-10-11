from . import source_indexer
from .source_indexer import SourceIndexer
import inspect
import logging, os

_init_config = {

    'caller_path' : None
}

_source_indexer = None

def init():
    global _init_config
    global _source_indexer

    if _init_config['caller_path'] is not None:
        error_message = 'initialize for the second time, why?'
        logging.error(error_message)

    (frame, script_path, line_number,
     function_name, lines, index) = inspect.getouterframes(inspect.currentframe())[1]




    _init_config['caller_path'] = os.path.realpath(script_path)

    SourceIndexer.prepare(_init_config)
    _source_indexer = SourceIndexer()




def _check_initialized():
    global _init_config
    global _source_indexer
    if _init_config['caller_path'] is not None:
        error_message = 'source manager is not initialized. call init() first'
        logging.error(error_message)
        raise Exception(error_message)

    if _source_indexer is None:
        error_message = 'something went wrong when initializing the source manager'
        logging.error(error_message)
        raise Exception(error_message)


def find():
    global _source_indexer
    _check_initialized()
    return _source_indexer

# find = _source_indexer.refresh()
# at = find.at


#
# class Compiler:
#
#     def __init__(self, component):
#         self.component = component
#
#     def to_palla(self):
#         print('PALLA {0}'.format(self.component.name))
#         return 'palla'
#


# indices = _source_indexer.indices.ok

# compiler = Compiler

def from_this():
    (frame, script_path, line_number,
     function_name, lines, index) = inspect.getouterframes(inspect.currentframe())[1]

    indexer = _source_indexer
    return indexer.at_path(script_path)







#
# #add all the attributes of the main package to the init.py for access
# _current_module = sys.modules[__name__]
#
#
# for i in dir(main):
#     if not i.startswith('__'):
#         setattr(_current_module, i, getattr(main, i))
#

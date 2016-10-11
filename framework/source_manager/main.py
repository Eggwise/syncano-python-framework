from . import source_indexer
from . import source_manager

_source_indexer = source_indexer.SourceIndexer()
find = _source_indexer.refresh()
at = find.at



class Compiler:

    def __init__(self, component):
        self.component = component

    def to_palla(self):
        print('PALLA {0}'.format(self.component.name))
        return 'palla'





indices = _source_indexer.indices.ok

compiler = Compiler

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

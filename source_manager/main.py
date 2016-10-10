from . import source_indexer
import inspect


_source_indexer = source_indexer.SourceIndexer()
find = _source_indexer.ok
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

    indexer = _source_indexer.ok
    return indexer.with_path(script_path)



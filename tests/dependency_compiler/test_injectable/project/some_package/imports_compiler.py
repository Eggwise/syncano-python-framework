from framework.compilers.base_compiler import CompilerBase
from framework.models.indexer import Source, IndexedItem
import sys, re, io, logging


class ImportCompiler(CompilerBase):


    get_import_source_code_execution_template = '''import inspect
{import_statement}
import_source_code = inspect.getsource({import_name})
print(import_source_code)
    '''


    def compile(self, item: IndexedItem) -> Source:

        return self._generate_import_sourcecode(item.source)



    @classmethod
    def _generate_import_sourcecode(cls, source: Source):
        generated_sources = []
        #injectable_import = namedtuple('tuple', ['line_number', 'import_name' ,'import_statement'])

        for line_number, line in enumerate(source):
            if len(line.strip()) ==0:
                continue

            # TODO TEST FOR ALL TYPE OF IMPORT STATEMENTS
            # TODO TESTSS
            try:
                import_name = line[line.index('import'):len(line)].split()[1]
                logging.info('extracted import statement with name: {0}'.format(import_name))
            except Exception:
                err_msg = 'could not extract import name from import statement: {0}'.format(line)
                logging.error(err_msg)
                raise Exception(err_msg)

            injected_source_code = cls._get_import_sourcecode(line, import_name)
            generated_sources.append(injected_source_code)

        return Source(generated_sources)

    @classmethod
    def _get_import_sourcecode(cls, import_statement, import_name):

        template_args = dict(import_statement=import_statement, import_name=import_name)
        execution_source = cls.get_import_source_code_execution_template.format(**template_args)


        logging.info('EXECUTING IMPORT STATEMENT {0}'.format(import_statement))

        # capture output
        original_stdout = sys.stdout
        redirected_output = sys.stdout = io.StringIO()
        exec(execution_source)
        sys.stdout = original_stdout

        import_source_code = redirected_output.getvalue()

        return import_source_code



compiler = ImportCompiler()
import inspect, os
from dev import source_manager




class SourceManagerBase():

    @classmethod
    def from_this(cls):
        (frame, script_path, line_number,
         function_name, lines, index) = inspect.getouterframes(inspect.currentframe())[1]
        print(script_path)
        return


    @classmethod
    def source_from_this(cls):
        (frame, script_path, line_number,
         function_name, lines, index) = inspect.getouterframes(inspect.currentframe())[1]

        with open(script_path) as script_file:
            script_source = script_file.read()
        if not script_source:
            raise Exception('could not open the source file at path: {0}'.format(script_path))


        return script_source

    @classmethod
    def source_from_this(cls):
        return cls._source_from_outer_frame(inspect.currentframe())

    @classmethod
    def _source_from_outer_frame(cls, current_frame):
        (frame, script_path, line_number,
         function_name, lines, index) = inspect.getouterframes(current_frame)[1]

        with open(script_path) as script_file:
            script_source = script_file.read()

        if not script_source:
            raise Exception('could not open the source file at path: {0}'.format(script_path))

        return script_source

    @classmethod
    def _path_from_outer_frame(cls, current_frame):
        (frame, script_path, line_number,
         function_name, lines, index) = inspect.getouterframes(current_frame)[1]

        return script_path
        pass

    @classmethod
    def _write_to(cls, path, source):
        with open(path, 'w') as f:
            f.write(source)


    @classmethod
    def source_lines_from_this(cls):
        source_lines = cls._source_from_outer_frame(inspect.currentframe()).splitlines(keepends=True)
        return source_lines

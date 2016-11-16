import datetime
import importlib.util
import logging
import os


class SourceManagerBase():
    pass



#TODO TEST
class FileManager(SourceManagerBase):


    DEFAULT_FILENAME = '{name}.{h}_{m}_{s}.{extension}'

    @classmethod
    def from_file(cls, file):
        return cls(file=file)

    def __init__(self, file):
        self._file = file

    @property
    def file(self):
        return self._file

    def importt(self):
        spec = importlib.util.spec_from_file_location(self.file.name, self.file.path)
        imported_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(imported_module)
        return imported_module


    def write_to(self, folder=None, name=None, path=None, override=False):
        return self._write_to(self.file, folder, name, path, override)

    @classmethod
    def _write_to(cls, source_component, folder=None, name=None, path=None, override=False):

        if path is not None:
            if folder is not None or name is not None:
                warn_message = 'write to path overiddes the folder & name parameter!'
                logging.warning(warn_message)
        else:

            if name is None:
                #take current filename
                now = datetime.datetime.now()

                name_format_args = {
                    'name': source_component.filename,
                    'h': now.hour,
                    'm': now.minute,
                    's': now.second,
                    'extension': source_component.extension
                }
                name = cls.DEFAULT_FILENAME.format(**name_format_args)

            if folder is None:
                folder = source_component.folder

            path = os.path.join(folder, name)


        #TODO more checks for existence of folder etc

        if os.path.exists(path) and not override:
            error_message = 'trying to write to existing path, {0} \n if you whish to override use the override parameter.'.format(path)
            logging.error(error_message)
            raise Exception(error_message)

        with open(path, 'w') as output_file:
            output = source_component.source
            output_file.write(output)
            return path


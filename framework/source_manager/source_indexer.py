import inspect
import logging
import os
import re

from framework.models.indexer import IndexedFile, SourceFile, IndexedItem, Source, Indexed, Index, Indices, Printable, SourceComponentContainer
from ..utils import find_dirs, merge, LOG_CONSTANTS




# @pretty_print
class SourceIndexerBase:

    CALLER_DIR = None

    @classmethod
    def prepare(cls, init_config):

        caller_path = init_config['caller_path']
        caller_dir = os.path.dirname(caller_path)
        logging.info('PREPARE SOURCE INDEXER')
        logging.info('-------------------------')
        logging.info('Source indexer initialized from script at: >> {0} <<'.format(caller_path))
        logging.info('The following dir will be used to seach the root config from: >> {0} <<'.format(caller_dir))


        cls.CALLER_DIR = caller_dir
        return cls



    config = {
        # root config for identifying the root config file in the workspace
        'config': {
            'identifier': '.config$'
        },
        'root_config_name': 'root.config',
    }

    @staticmethod
    def extract_name(path, identifier):
        path = os.path.realpath(path)
        extract_regex = '(?P<name>.*){0}'.format(identifier)
        parent, filename = os.path.split(path)
        name_match = re.match(extract_regex, filename)

        assert name_match is not None
        assert 'name' in name_match.groupdict()
        assert name_match.groupdict()['name']

        return name_match.groupdict()['name']

    @classmethod
    def _get_root_config_path(cls):
        logging.info('Searching for root config path..')
        logging.info('Walking up from the dir: {0}'.format(cls.CALLER_DIR))
        indexer_location = cls.CALLER_DIR

        config_identifier = cls.config['config']['identifier']
        root_config_name = 'root'
        root_config_identifier = root_config_name + config_identifier

        root_dir_search = find_dirs(indexer_location, root_config_identifier)
        if len(root_dir_search) == 0:
            error_message = 'NO ROOT CONFIG\nCould not find root config file\n searched from {0} \n upwards..'.format(indexer_location)
            logging.error(error_message)
            raise Exception(error_message)
        root_config_path = root_dir_search[0]

        logging.info('Root config found at: {0}'.format(root_config_path))
        return root_config_path

    @classmethod
    def _get_root_dir(cls):
        return os.path.dirname(cls._get_root_config_path())

    @classmethod
    def _get_root_config(cls):
        logging.info('Getting the root config..')
        root_config_path = cls._get_root_config_path()
        #extract the name from the root config
        #using the hardcoded index described in the config attribute of the class
        root_config_name = cls.extract_name(root_config_path, cls.config['config']['identifier'])

        #if ever this assertion fails... something is terribly wrong
        assert root_config_name == 'root'
        return SourceFile(root_config_name, root_config_path)

    @classmethod
    def _get_paths_by_identifiers(cls, identifiers: list):
        root_dir = cls._get_root_dir()

        if len(set(identifiers)) < len(identifiers):
            print('WARNING: CHECKING FOR MATCHES WITH SAME IDENTIFIER')
            print('YOU WILL LOSE YOUR INDEX')
            print('YOU PROBABLY NEED TO WRITE A NEW METHOD IF YOU NEED TO INDEX MULTIPLE INDICES WITH SAME IDENTIFIER')

        matches_by_identifier = {k: [] for k in identifiers}
        for path, dirs, files in os.walk(root_dir):
            for identifier in identifiers:
                matches = [os.path.join(path, i) for i in dirs + files if str(i).endswith(identifier)]
                matches_by_identifier[identifier].extend(matches)

        return matches_by_identifier

    @classmethod
    def _get_indices(cls):
        logging.info('Retrieving indices')
        # get identifiers

        root_config = cls._get_root_config()
        root_index_config = root_config.yaml['index']

        if 'identifiers' not in root_index_config:
            msg = 'MISSING IDENTIFIERS FOR INDICES TYPES IN ROOT INDEX CONFIG\n turn on logging to see more..'
            logging.error(msg)
            raise AttributeError(msg)

        # flip
        identifiers_with_types = {v: k for k, v in root_index_config['identifiers'].items()}

        # get identifier list
        identifiers = [v for k, v in root_index_config['identifiers'].items()]
        index_types = root_index_config['types']

        if not len(identifiers) == len(index_types):
            msg = 'NO IDENTIFIERS DEFINED FOR THE INDEX TYPES IN THE ROOT INDEX CONFIG\n\nthe following index types are defined\n' \
                  '{0}'.format(index_types) + \
                '\nthe following identifiers are defined: {0}\n'.format(root_index_config['identifiers'].items()) +\
                'Check your root config file at: {0}'.format(root_config.path)
            logging.error(msg)
            raise Exception(msg)


        indices = []
        # get paths for indices
        indexed_paths = cls._get_paths_by_identifiers(identifiers)
        for identifier, paths in indexed_paths.items():
            # order them by type
            # indices_by_type[identifiers_with_types[identifier]] = paths
            for p in paths:
                index_name = cls.extract_name(p, identifier)
                index_config_file = SourceFile(name=index_name, path=p)
                index = Index(index_name, identifiers_with_types[identifier], index_config_file)
                indices.append(index)

        # merge parent configs for indices
        # order root configs by type
        base_index_configs = {i.index_type: i for i in indices if i.name == 'root'}

        if len(base_index_configs) != len(index_types):
            print('MISSING BASE INDEX FILE FOR {0}'.format([i for i in index_types if i not in base_index_configs]))
            raise Exception()
        merged_indices = []
        for index in [i for i in indices if i.name != 'root']:
            parent_config = base_index_configs[index.index_type]

            #TODO
            merged_config_dict = merge(parent_config.config, index.config)
            merged_index_config = SourceFile(name=index.name, path=index.config_file.path, source=Source.from_yaml(merged_config_dict))

            index = Index(name=index.name, index_type=index.index_type, config_file=merged_index_config)
            merged_indices.append(index)
        return Indices(merged_indices)

    @classmethod
    def _index_files(cls, indices: Indices):
        identifiers_with_indices = {}
        assert all(list(map(lambda x: x.index_type == 'file', indices)))


        ## for now just do the file types and get the items from the files later
        file_indices = [i for i in indices if i.index_type == 'file']
        # file_indices = [i for i in indices]
        for i in file_indices:

            if not isinstance(i.identifier, str):
                error_message = 'trying to index files using non file indices \n' \
                                + 'are you sure the index config file is correct ?\n' \
                                + 'for files use a string as identifier\n' \
                                + 'Indices used: \n{0}'.format(indices._print)
                logging.error(error_message)
                raise Exception(error_message)

            if 'identifier' not in i.config:
                print('NO IDENTIFIER FOR INDEX: {0}'.format(i.name))
                raise Exception()
            ##TODO
            identifiers_with_indices[i.identifier] = i
        assert isinstance(indices, Indices)
        # indices = []
        indexed_paths = cls._get_paths_by_identifiers(list(identifiers_with_indices.keys()))

        files = []
        for identifier, paths in indexed_paths.items():

            # order them by type
            # indices_by_type[identifiers_with_types[identifier]] = paths
            for p in paths:
                indexed_file_name = cls.extract_name(p, identifier)
                index = identifiers_with_indices[identifier]
                assert isinstance(index, Index)
                indexed_index_file = IndexedFile(indexed_file_name, p, index)
                files.append(indexed_index_file)

        return Indexed(files)


class ItemIndexer(SourceIndexerBase):



    @staticmethod
    def parse_identifier_arguments(identifier_arguments, identifier_string, start=True):
        # get the tags from the identifier string,
        # some of the tags are named with the following format->  {tag:name}

        identifier_tags = re.findall('{([a-z:_.A-Z]*)}', identifier_string)

        named_regex_template = '(?P<{name}>{regex})'
        format_arg_dict = {}

        for an in identifier_tags:
            arg, *arg_name = an.split(':')

            if arg not in identifier_arguments:
                if start:
                    raise KeyError('MISSING ARGS FOR {0}'.format(arg))
                else:
                    # if this is the end tag, then the named tags in the start identifier
                    # will be injected after extracting the item from the source
                    # so for now keep keep the {name} in the string
                    identifier_arguments[arg] = '{' + str(arg) + '}'

            if arg_name:
                arg_name = arg_name[0]
                # replace the named arg so the string can be formatted
                identifier_string = identifier_string.replace(':{0}'.format(arg_name), '')
                arg_value = named_regex_template.format(name=arg_name, regex=identifier_arguments[arg])
            else:
                arg_value = identifier_arguments[arg]

            format_arg_dict[arg] = arg_value

        # return identifier_string, format_arg_dict
        identifier = identifier_string.format(**format_arg_dict)
        return identifier

    @classmethod
    def _extract_items(cls, indexed_file: IndexedFile, indices: Indices):
        logging.info('Extracting items from:')
        # logging.info(LOG_CONSTANTS.REGION.format('EXTRACT ITEMS'))
        indexed_file.log()
        all_extracted_items = []
        # TODO VALIDATE ?
        for i in indices:
            if i.index_type != 'item':
                logging.error('Trying to extract items from non item index: {0}'.format((i.name, i.index_type)))
            assert i.index_type == 'item'
            config = i.config
            parse_tags = config['parse_tags']
            identifier_start_config = i.identifier['start']

            # TODO does this work???
            if 'end' in config['identifier']:
                identifier_end_config = i.identifier['end']
            else:
                logging.info('no end tag provided')
                logging.info('getting default end identifier tag from root.item.index')
                if 'end_default' not in parse_tags:
                    error_message = 'Could not find default end identifier tag'
                    logging.error(error_message)
                    raise Exception(error_message)
                identifier_end_config = parse_tags['end_default']

            format_arg_values = merge(config, parse_tags)

            start_identifier = cls.parse_identifier_arguments(format_arg_values, identifier_start_config)
            # NOT SURE IF THE SAME END IDENTIFIER AS START_IDENTIFIER WORKS
            end_identifier = cls.parse_identifier_arguments(format_arg_values, identifier_end_config, False)

            extracted_items = cls._extract_items_from_source(start_identifier, end_identifier, indexed_file, i)
            all_extracted_items.extend(extracted_items)
        logging.info('found {0} items'.format(len(all_extracted_items)))
        logging.info('\n')
        return all_extracted_items

    @staticmethod
    def _extract_items_from_source(start_match_regex, end_match_regex, indexed_file: IndexedFile, item_index: Index):
        source = indexed_file.source

        def get_line_number(the_match):
            return source.count("\n", 0, the_match.start()) + 1

        # loop over start matches and get the corresponding end match
        # then create item
        items = []

        start_matches = re.finditer(start_match_regex, source)

        for start_match in start_matches:
            line_start = get_line_number(start_match)
            match_props = start_match.groupdict()
            # print(end_match_regex)

            try:
                end_regex = end_match_regex.format(**match_props)
            except Exception:
                error_message = 'could not format the end tag using the named tags in the start identifier\n'\
                'Tried to format the string: {0} using the available arguments: {1}\n'.format(end_match_regex, match_props) \
                + 'If you dont want to use a end identifier leave the end attribute empty in ' \
                        'the identifier options in your index config \nthe standard end identifier in the '\
                'root item index config will be used.. normally matching 1 or more whitespaces ( {ws}+ )'

                logging.error(error_message)
                raise Exception(error_message)
            # check for end of item matches
            assert isinstance(source, Source)

            source_from_start_match = source[line_start:]

            line_end = None
            for index, line in enumerate(source_from_start_match):
                if re.match(end_regex, line):
                    line_end = line_start + index
                    break
            if line_end is None:
                # No end tag found for dependency section
                error_message = 'Could not find end of region for: {0}'.format(end_regex)
                logging.error(error_message)
                print(error_message)
                raise Exception(error_message)

            if 'name' not in match_props:
                error_message = 'a name must be defined for an item index\n' \
                                'include the name tag {name} somewhere in the start identifier string for matching' \
                                'available variables {0}'.format(match_props) +\
                                'NOTE: the tags in the start identifier are available in the end identifier'
                logging.error(error_message)
                raise AttributeError(error_message)

            name = match_props['name']
            del (match_props['name'])

            item = IndexedItem(name, indexed_file, line_start, line_end, item_index, properties=match_props)
            items.append(item)

        return items





# @pretty_print
class SourceIndexer(ItemIndexer, Printable, SourceComponentContainer):

    TIMES_INDEXED = 0

    _all_indexed = None

    def __init__(self, indices: Indices=None, scoped: Indexed = None, index_all=True):
        self.indices = indices or self._get_indices()
        if index_all:
            SourceIndexer._all_indexed = self._index_all()

        # if scoped is not None:
        #     self.scoped = Indexed(scoped)
        # else:
        #     self.scoped = Indexed(self.all_indexed)

        self.scoped = scoped or self.all_indexed
        self.current = 0

    def __getattr__(self, name):
        return self.filter(lambda x: x.match(name))



    def __getitem__(self, item):
        if isinstance(item, slice):
            self.scoped = Indexed(self.scoped[item.start, item.stop])
            return self

        logging.debug('get item {0} from source indexer, passing it to the scoped indexed components'.format(item))
        return self.scoped[item]


    @property
    def copy(self):
        return SourceIndexer(indices=Indices(self.indices.scoped), scoped=Indexed(self.scoped), index_all=False)

    @property
    def all_indexed(self):
        return SourceIndexer._all_indexed

    def _index_all(self):
        SourceIndexer.TIMES_INDEXED += 1

        if SourceIndexer.TIMES_INDEXED > 1:
            error_message = 'indexing all the source for the second time, why???'
            logging.error(error_message)
            raise Exception(error_message)

        logging.info(LOG_CONSTANTS.REGION.format('INDEXING ALL SOURCE'))
        # self.indices.refresh()
        item_indices = self.indices.item.ok
        file_indices = self.indices.file.ok

        file_indices.log()

        all_indexed_files = self._index_files(file_indices)
        all_indexed_files.log()

        #TODO
        all_indexed_items = []
        for file in all_indexed_files:
            indexed_items = self._extract_items(file, item_indices)
            all_indexed_items.extend(indexed_items)

        all_indexed = Indexed(all_indexed_items, all_indexed_files)
        logging.info(LOG_CONSTANTS.REGION.format('INDEXING END'))
        logging.info(
            'indexed {0} source components using {1} indices'.format(len(all_indexed), len(self.indices)))

        return all_indexed

        # def _apply_filter(self, filter_func):
        # self.scoped = list(filter(filter_func, self.scoped))

    @property
    def _print(self):
        return LOG_CONSTANTS.REGION_IDENTIFIER \
        + LOG_CONSTANTS.REGION.format('SOUCE_INDEXER') \
        + LOG_CONSTANTS.LINE.format('Amount of indices: {0}'.format(len(self.indices))) \
        + LOG_CONSTANTS.LINE.format('Total amount of indexed source components: {0}'.format(len(self.all_indexed))) \
        + LOG_CONSTANTS.LINE.format('source components in scope: {0}'.format(len(self.scoped))) \
        + LOG_CONSTANTS.LINE.format(LOG_CONSTANTS.REGION.format('SOUCE_INDEXER END')) \
        + LOG_CONSTANTS.REGION_IDENTIFIER





    def refresh(self):
        self.indices.refresh()
        self.scoped = self.all_indexed
        return self


    # def get(self, one=True):
    #     logging.info('get call from source indexer, passing it to the scoped indexed components')
    #     return self.scoped.get(one=one)

    @property
    def count(self):
        return len(self.scoped)


    def __len__(self):
        return len(self.scoped)


    def list(self):
        print(LOG_CONSTANTS.REGION.format('LIST INDEXED COMPONENTS'))
        for i in self:
            if hasattr(i, '_print'):
                i.print()
            else:
                print(i)

        print(LOG_CONSTANTS.REGION.format('LIST INDEXED COMPONENTS END'))
        pass

    def at_path(self, path, temp_index=False, mutable=False):

        if temp_index:
            #create index
            #create indexed file
            #index the items in this file
            #add to scope
            raise NotImplementedError
            pass

        if mutable:
            return_val = self
        else:
            return_val = self.copy

        return_val = return_val.filter(lambda x: x.path == path, mutable)
        # print(return_val.ok)
        if len(return_val) == 0:
            error_message = 'Trying to get indexed components with path: {0}\n' \
                            'But no indexed components could be found with the current indices\n' \
                            'Are you sure you are calling from_this() from within an indexed file?\n' \
                            'Available indices: \n{1}'.format(path, self.indices._print)
            logging.error(error_message)
            raise Exception(error_message)

        return return_val


    @property
    def items(self):
        return self.filter(lambda x: x.index.index_type == 'item')


    @property
    def files(self):
        return self.filter(lambda x: x.index.index_type == 'file')

    @property
    def components(self):
        return self.scoped.components


    @property
    def here(self):
        (frame, script_path, line_number,
         function_name, lines, index) = inspect.getouterframes(inspect.currentframe())[1]
        print(script_path)
        return self.at_path(script_path)

    def at(self, *source_components):
        #TODO file indexer at DIR

        source_components = Indexed(*source_components)
        source_components_with_paths = []
        for c in source_components:

            #for now compare with path, later check folder too
            for s in self.scoped:
                if s.is_at(c):
                    if s not in source_components_with_paths:
                        source_components_with_paths.append(s)

        instance = SourceIndexer(scoped=Indexed(*source_components_with_paths), index_all=False)
        return instance

    def extract_items(self, keep_scope=True):
        #TODO TEST
        files = self.files.get(one=False)
        indices = self.indices.item.ok

        extracted_items = [self._extract_items(f, indices) for f in files]
        self.scoped = Indexed(extracted_items)
        return self


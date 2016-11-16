from framework.models.indexer import Indexed, SourceComponent


class CompilerBase():


    def compile(self, source_component: SourceComponent):
        raise NotImplementedError

    def compile_all(self, source_components: Indexed):
        raise NotImplementedError


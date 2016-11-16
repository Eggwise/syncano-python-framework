from framework import source_manager
from framework.compilers.imports_compiler import ImportCompiler
from framework.models.indexer import Indexed, IndexedItem
import logging


#uncomment to see what happens
# logging.basicConfig(level=1)


IMPORT_STATEMENT = 'from tests.dependency_compiler.test_injectable.project.some_package.test_class import Person'

source_manager.init()


#scope to the injectable items in this file
injectable_classes = source_manager.from_this().injectable.classes
#or use
injectable_classes = source_manager.find().injectable.classes.here
injectable_classes = source_manager.find().here.injectable.classes # or whatever order..


#make sure we have the right items
injectable_classes.list()

#confirm and get indexed components
injectable_classes = injectable_classes.ok # type: Indexed

#Indexed is a component container

#for this test we only inject in one item
injectable_class = injectable_classes.one # type: IndexedItem


#use OK to get scoped components
#so you can do it like this


##injectable_classes = injectable_classes.ok # type: List[IndexedItem]
#get list of components
##injectable_class = injectable_classes[0]

print('\n\nPRINT INJECTABLE CLASS\n\n')
injectable_class.print()

# print('\n\nPRINT INJECTABLE CLASS SOURCE')
# print(injectable_class.source)
# print(IMPORT_STATEMENT)

#this fails, check parsing using whitespace
#assert len(IMPORT_STATEMENT) == len(injectable_class.source)

## GET COMPILER


##TODO MAKE COMPILERS AVAILABLE FROM FRAMEWORK PACKAGE
#TO USE THE FRAMEWORK GIT CLONE IT ABOVE THE ROOT CONFIG SO EVERY COMPILER CAN BE INDEXED
print('dude' , source_manager.find().python.files)

dep_compilers = source_manager.find().imports.compiler.ok




dep_compiler_file = dep_compilers.one
dep_compiler_module = dep_compiler_file.importt()
#
# dep_compiler.generate_import_sourcecode(injectable_class.lines)
#


dep_compiler = dep_compiler_module.compiler # type: ImportCompiler

generated_source = dep_compiler.compile(injectable_class)

print(generated_source)

#IMPORT STATEMENT here




#imported classes
from tests.dependency_compiler.test_injectable.project.some_package.test_class import Person


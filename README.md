# syncano-python-framework
Code your source (code), ez customizable python and syncano development framework (WIP)

Features
---
- Create indexes for your type of files
- Use your source as if it is a python class, (straight forward workflows for compiling, debugging, deploying)
- Custom generators for models, scripts, projects, packages, you name it.)
- Dependency injection (example: for injecting your models in your scripts and compile to deployment folder)
- Python model generating from yaml configs
- Tracable/debug script compiler for online debug results. something like https://github.com/mihneadb/python-execution-trace
- yuml compiler (create uml diagrams from ur classes, and use dep injection for importing them to create nice uml diagrams) (see http://yuml.me/)


Dependency injection ?? :D
---
Define custom indexes which you can use in your source to create dependencies.
Indexes ? check explanation after example.


Example
---
A simple example of what you can do with this stuff
as if i where you, jo.

I create a person class dependency.
I mark the dependency using the #dep.start tag (this is customizable) 
(you can mark & compile anything in any file (or any file), but for now i use a python dependency as an example)

**person.model.py**
```
#dep.start PersonModel

class Person(SyncanoObject):
  ....
  ....
  
#dep.end 


```


Then in my awesome script you can develop like you normally would
and compile it to scripts hosted on syncano.


**test.script.py**
```
from models import PersonModel
from project import source

source.from_this().region('epic_script').inject.write('custom_name').deploy()
source.stop


#region.start epic_script

#inject PersonModel

(OR JUST USE)
---
#injectable
from models import PersonModel
--

person = PersonModel(**ARGS)
person.name = 'test'
person.save

#region.end epic_script



```
In this script i created an indexed item using the 'region' index and my . 
This is the region i want to be compiled for deployment on my syncano instance.

I mark the injection point for the person model.
Or (more ez) i tag the import i want to be injected in my script at compilation.

Then at the top of script i get the source manager from this script
now i got the manager pointing at my script.
i select the region i want to be compiled
i inject the dependencies 
i write to a custom file
i then deploy the script





Indexing ??
---
It is possible to define your own indexes for
- projects
- packages
- files
- items (regions in files)

The framework automaticly generates the python code for the manager which you can use to interact with your indexed files.
Using compilers it is possible to compile your indexed sources to for example.
- syncano python models (ORM for your syncano classes)
- scripts with injected source code (for example your models, custom functions etc)
- compile your scripts and write them to the syncano cli script folder for synchronization


**No restrictions where your source files/dirs are located. **
index your files with .index files and use your source manager to compile it to the format you whish.
working on documentation compiler as well, to easily generate docs for on github.



Compilers:
---
- debug compiler
- imports injection compiler
- python model copiler
- yuml diagram compiler


Dependency injection compiler:
Inject code in your scripts and generate scripts that get deployed on syncano.


Debug compiler:
with this compiler you can compile your python script to a tracable script which records everything when the script is executed and creates a debuggable json file which you can use in an app to track exactly what happened in your script when it ran (save these files to your syncano project so you can track errors, attacks, bugs)



**seamless integration with syncano-cli for ez development.**

**WORK IN PROGRESS** 
WIP WIP WIP


**thanks for reading**

cheers


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

**no matter where and how/what your source is, manage and transform/compile it how you whish**

# UPDATE
This framework is build using the source framework: https://github.com/Eggwise/source_framework
ATM, dont use this repo. the code will soon be split up to make it usable.
to check out the source framework. clone the source framework test repo
https://github.com/Eggwise/source_framework_test

run generate_test.py to setup the framework
then checkout the other test files.


more examples, documentation and compilers coming soon,






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


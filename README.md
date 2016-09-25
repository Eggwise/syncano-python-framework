# syncano-python-framework
Code your source (code), ez customizable python and syncano development framework (WIP)

Features
- Create indexes for your type of files
- Use your source as if it is a python class, (straight forward workflows for compiling, debugging, deploying)
- Custom generators for models, scripts, projects, packages, you name it.)
- Dependency injection (example: for injecting your models in your scripts and compile to deployment folder)
- Python model generating from yaml configs
- Tracable/debug script compiler for online debug results. something like https://github.com/mihneadb/python-execution-trace
- yuml compiler (create uml diagrams from ur classes, and use dep injection for importing them to create nice uml diagrams) (see http://yuml.me/)


Indexing
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

I am working on several compilers
---
Dependency injection compiler:
Inject code in your scripts and generate scripts that get deployed on syncano.


Debug compiler:
with this compiler you can compile your python script to a tracable script which records everything when the script is executed and creates a debuggable json file which you can use in an app to track exactly what happened in your script when it ran (save these files to your syncano project so you can track errors, attacks, bugs)



Compilers:
---
- debug compiler
- imports injection compiler
- python model copiler
- yuml diagram compiler

seamless integration with syncano-cli for ez development.

WIP WIP WIP


# Another init file.
from importlib import import_module
from pkgutil import walk_packages

for _, name, _ in walk_packages(__path__):
    import_module(f'commands.{name}')

del import_module, walk_packages

from __future__ import print_function
from glob import glob
import keyword
import re
import sys
import os
import stat
from os.path import dirname, join, split, splitext

sys.path.insert(1, os.path.join(sys.path[0], "'.."))


def isidentifier(s):  # to make this work with Python 2.7.
    if s in keyword.kwlist:
        return False
    return re.match(r'^[a-z_][a-z0-9_]*$', s, re.I) is not None

basedir = dirname(__file__)
os_name = os.name

__all__ = []
for name in glob(join(basedir, u"*.py")):
    module = splitext(split(name)[-1])[0]
    if not module.startswith(u"_") and isidentifier(module) and not keyword.iskeyword(module):
        if os_name == u"posix":
            st = os.stat(name)
            if (bool(st.st_mode & stat.S_IXGRP) 
                or module == u"mobile_app" 
                or module == u"plugin_manager"
                ):  # Load plugin if group permission is executable.
                try:
                    __import__(__name__ + u"." + module)
                except Exception as e:
                    print(u"Ignoring exception while loading the {} plug-in.".format(module))
                    print(e)  # Provide feedback for plugin development
                else:
                    __all__.append(module)       
        elif os_name == u"nt":
            try:
                __import__(__name__ + "." + module)
            except Exception as e:
                print(u"Ignoring exception while loading the {} plug-in.".format(module))
                print(e)  # Provide feedback for plugin development
            else:
                __all__.append(module)
__all__.sort()
# print("__all__: ", __all__) #  test
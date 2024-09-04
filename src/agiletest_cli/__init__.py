# this is to fix mkdocs import issue
import os
import sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)))

from .main import cli

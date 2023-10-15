import os
import sys


def apply():
    current_dir = os.path.abspath(os.path.dirname(__file__))

    parent_dir = os.path.join(current_dir, "..")
    sys.path.insert(0, parent_dir)

    lib_dir = os.path.join(parent_dir, "demo_updater")
    sys.path.insert(0, lib_dir)

import sys
import os

# Get the root directory of the project (where todo_app package is)
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
print(f"Adding {root_dir} to sys.path")
sys.path.insert(0, root_dir)

# Now todo_app can be imported as a package 
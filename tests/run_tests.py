import unittest
import sys
import os

# Add the project root directory to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Discover and load all test cases in the current directory
loader = unittest.TestLoader()
tests = loader.discover(os.path.dirname(__file__))

# Run the tests
runner = unittest.TextTestRunner(verbosity=2)
result = runner.run(tests)

# Set the exit code based on test success
sys.exit(not result.wasSuccessful())

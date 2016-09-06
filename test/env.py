import os
import sys

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
UNIT_TEST_DIR = os.path.join(ROOT_DIR, "unit")
ACCEPTANCE_TEST_DIR = os.path.join(ROOT_DIR, "acceptance")
RESOURCES_DIR = os.path.join(ROOT_DIR, "resources")
TEST_LIBS_DIR = os.path.join(RESOURCES_DIR, "testlibs")
RESULTS_DIR = os.path.join(ROOT_DIR, "results")
HTTP_SERVER_FILE = os.path.join(RESOURCES_DIR, 'testserver', 'testserver.py')
SRC_DIR = os.path.join(ROOT_DIR, "..", "src")

sys.path.insert(0, SRC_DIR)
sys.path.append(UNIT_TEST_DIR)

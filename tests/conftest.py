import pytest
import json
import os
from dotenv import load_dotenv


pytest.testDirectory = os.path.dirname(os.path.abspath(__file__))

@pytest.fixture(scope='session', autouse=True)
def load_env():
    load_dotenv()

def pytest_configure(config):
    loadAllJsonData()



def loadAllJsonData():
    jsonDirectory = os.path.join(pytest.testDirectory, 'data')
    pytest.JSON_DATA = {}
    for filename in os.listdir(jsonDirectory):
        if filename.endswith('.json'):
            file_path = os.path.join(jsonDirectory, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                key = os.path.splitext(filename)[0]
                pytest.JSON_DATA[key] = json.load(file)
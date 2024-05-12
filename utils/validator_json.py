import json
import allure
from utils import resource
from jsonschema import validate


@allure.step('API: validate JSON scheme')
def validator_json_scheme(resp, name):
    schema = json.load(open(resource.path_json_scheme(file_name=name)))
    validate(resp, schema)
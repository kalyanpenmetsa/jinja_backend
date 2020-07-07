from flask import Flask, jsonify, request, render_template, abort
import json, os, sys, yaml, re, io
from flask_restful import reqparse
from jinja2 import Environment, BaseLoader, StrictUndefined
from jinja2_ansible_filters import AnsibleCoreFiltersExtension
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app) #Prevents CORS errors

@app.route("/render_jinja", methods=['POST'])
def render_jinja():
    try:
        parser = reqparse.RequestParser()
        parser.add_argument('jinja_input')
        parser.add_argument('jinja_variable')
        args = parser.parse_args()
        print(args)
        jinja_input, variable_input = args.get("jinja_input"), args.get("jinja_variable")
        variable_type = JsonOrYaml(variable_input)
        output = render_jinja(jinja_input, variable_input, variable_type)
        print(output)
    except Exception as error:
        abort(400, error)
        raise
    else:
        return output

def render_jinja(jinja_input, variable_input, variable_type):
    try:
        if variable_type == 'json':
            variable_input = json.loads(variable_input)
        elif variable_type == 'yaml':
            variable_input = yaml.load(variable_input)
        template = Environment(loader=BaseLoader, extensions=[AnsibleCoreFiltersExtension], trim_blocks=True, lstrip_blocks=True, undefined=StrictUndefined).from_string(jinja_input)
        output = template.render(variable_input)
    except Exception as error:
        raise
    else:
        return output

def JsonOrYaml(variable_input):
    def isJson(str):
        try:
            json.loads(str)
        except ValueError:
            return False
        else:
            return True

    def isYaml(str):
        try:
            yaml.load(str)
        except Exception as error:
            return False
        else:
            return True

    if isJson(variable_input):
        var_type = "json"
    elif isYaml(variable_input):
        var_type = "yaml"
    else:
        var_type = None
    return var_type

if __name__ == '__main__':
    app.run(debug=True)
    app.run(host='0.0.0.0')

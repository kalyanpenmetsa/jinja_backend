from flask import Flask, jsonify, request, render_template, abort
import json, os, sys, yaml, re, io
from flask_restful import reqparse
from jinja2 import Environment, BaseLoader, StrictUndefined
from jinja2_ansible_filters import AnsibleCoreFiltersExtension
from ansible.plugins.filter import ipaddr
from flask_cors import CORS
import logging
from logging.handlers import RotatingFileHandler
from flask_swagger import swagger

app = Flask(__name__)
cors = CORS(app) #Prevents CORS errors
app.config.from_pyfile('application.conf', silent=False)
if not os.path.exists("logs"): os.makedirs("logs")
handler = RotatingFileHandler(app.config.get("LOG_LOCATION"), maxBytes=10000, backupCount=1)
handler.setFormatter(logging.Formatter(app.config.get("LOG_FORMAT")))
app.logger.setLevel(logging.DEBUG)
app.logger.addHandler(handler)

@app.route("/render_jinja", methods=['GET', 'POST'])
def render_jinja():
    if request.method == "POST":
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('jinja_input')
            parser.add_argument('jinja_variable')
            args = parser.parse_args()
            jinja_input, variable_input = args.get("jinja_input"), args.get("jinja_variable")
            variable_type = JsonOrYaml(variable_input)
            output = render_jinja(jinja_input, variable_input, variable_type)
            app.logger.info("Successfully rendered the template.")
        except Exception as error:
            app.logger.error(error)
            abort(400, error)
            raise
        else:
            return output
    else:
        app.logger.error("GET Method invoked.")
        return jsonify({"status": True, "allowed": "POST"})

@app.route("/spec")
def spec():
    swag = swagger(app)
    swag['info']['version'] = "1.0"
    swag['info']['title'] = "Jinja Renderer"
    swag['paths']['Jinja Renderer'] = "/render_jinja"
    swag['paths']['info'] = "/spec"
    return jsonify(swag)

def render_jinja(jinja_input, variable_input, variable_type):
    try:
        if variable_type == 'json':
            variable_input = json.loads(variable_input)
        elif variable_type == 'yaml':
            variable_input = yaml.load(variable_input)
        ip_filter = ipaddr.FilterModule()
        template = Environment(loader=BaseLoader, extensions=[AnsibleCoreFiltersExtension], trim_blocks=True, lstrip_blocks=True, undefined=StrictUndefined).from_string(jinja_input)
        template.filters.update(ip_filter.filters())
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

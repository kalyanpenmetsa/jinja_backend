from main import app
import json, ast, os

def test_main_get():
    response = app.test_client().get('/render_jinja')
    response_data = json.loads(response.data.decode("UTF-8").replace("\n", ""))
    assert response.status_code == 200
    assert response_data["status"] == True
    assert response_data["allowed"] == "POST"

def test_main_post_json():
    for test_dir in os.listdir(os.path.join(os.getcwd(), "src", "test_data")):
        input = {
            "jinja_input": open(os.path.join(os.getcwd(), "src", "test_data", test_dir, "jinja_input.j2")).read(),
            "jinja_variable": json.loads(open(os.path.join(os.getcwd(), "src", "test_data", test_dir, "input.json")).read())
        }
        response = app.test_client().post('/render_jinja', json=input)
        assert response.status_code == 200
        assert response.data.decode("UTF-8") == open(os.path.join(os.getcwd(), "src", "test_data", test_dir, "jinja_output.txt")).read()

def test_main_post_yaml():
    for test_dir in os.listdir(os.path.join(os.getcwd(), "src", "test_data")):
        input = {
            "jinja_input": open(os.path.join(os.getcwd(), "src", "test_data", test_dir, "jinja_input.j2")).read(),
            "jinja_variable": open(os.path.join(os.getcwd(), "src", "test_data", test_dir, "input.yaml")).read()
        }
        response = app.test_client().post('/render_jinja', json=input)
        assert response.status_code == 200
        assert response.data.decode("UTF-8") == open(os.path.join(os.getcwd(), "src", "test_data", test_dir, "jinja_output.txt")).read()

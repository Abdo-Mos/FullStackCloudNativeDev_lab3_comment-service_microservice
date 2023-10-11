from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

# USR_URL_REQ =

comments = [
    {"id": 1, "user_id": 1, "post_id": 2, "comment": "Amazing post!"},
    {"id": 2, "user_id": 2, "post_id": 1, "comment": "Another amazing post!"},
]

@app.route('/')
def home_route():
    return jsonify(comments)
    return "Hello from comments server!"

# -R- read comment by id
@app.route('/comment/<id>')
def get_by_id(id):
    comment_info = None
    for comment in comments:
        if int(comment['id']) == int(id):
            comment_info = comment
            break
    
    usr_req_res = requests.get(f'http://127.0.0.1:5000/user/{comment_info["user_id"]}').json()
    post_req_res = requests.get(f'http://127.0.0.1:5001/post/{comment_info["post_id"]}').json()

    comment_info['user'] = usr_req_res
    comment_info['post'] = post_req_res
    
    return jsonify(comment_info)





if __name__ == '__main__':
    app.run(port=5002)
from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

# URL_usr_req  = 'https://userservicecontainer.wonderfulocean-aa423ae1.canadacentral.azurecontainerapps.io/user/'
# URL_post_req = 'https://postservicecontainer.wonderfulocean-aa423ae1.canadacentral.azurecontainerapps.io/post/'

URL_usr_req  = 'http://127.0.0.1:5000/user/'
URL_post_req = 'http://127.0.0.1:5001/post/'


comments = [
    {"id": 1, "user_id": 1, "post_id": 2, "comment": "Amazing post!"},
    {"id": 2, "user_id": 2, "post_id": 2, "comment": "Another amazing post!"},
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
    
    usr_req_res = requests.get(f'{URL_usr_req}{comment_info["user_id"]}')
    post_req_res = requests.get(f'{URL_post_req}{comment_info["post_id"]}')

    comment_info['user'] = usr_req_res.json()
    comment_info['post'] = post_req_res.json()
    
    return jsonify(comment_info)

# -C- craete comments
@app.route('/comment', methods=['POST'])
def craete_comment():

    usr_req_res = requests.get(f'{URL_usr_req}{request.json["user_id"]}').json()
    post_req_res = requests.get(f'{URL_post_req}{request.json["post_id"]}').json()

    new_comment = {
    "id": request.json['id'],
    "user_id": usr_req_res,
    "post_id": post_req_res,
    "comment": request.json['comment'] 
    }

    comments.append(new_comment)
    return jsonify({'Success': new_comment})

# -U- update comment
@app.route('/comment/<id>', methods=['PUT'])
def update_comment(id):
    a_comment = None

    for comment in comments:
        if int(comment['id']) == int(id):
            a_comment = comment
            break
    
    if a_comment == None:
        return jsonify({'error:': 'comment not found'})
    
    a_comment['comment'] = request.json['comment']
    return jsonify({'updated': a_comment})

# -D- delete comment
@app.route('/comment/<id>', methods=['DELETE'])
def delete_comment(id):
    a_comment = None

    for comment in comments:
        if int(comment['id']) == int(id):
            a_comment = comment
            break

    if a_comment == None:
        return jsonify({'error:': 'comment not found'})
    
    comments.remove(a_comment)
    return jsonify("Deleted successfully")

if __name__ == '__main__':
    app.run(port=5002)
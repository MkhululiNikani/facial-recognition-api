from flask import Flask, request
import face_recognition
from image import Image
from database import Database
from response import Response

app = Flask(__name__)

response = Response()
# TODO: use env variables
db = Database('127.0.0.1', 'nick', 'Gazorpazorp#2020', 'facial_recognition')


@app.route('/add-face', methods=['POST'])
def add_face():
    # If the user did not provide an image or user_id
    if not ('image' in request.files and 'fullname' in request.form):
        return response.bad_request('Missing parameters (image or fullname)')

    file = request.files.get('image')
    image = Image(file)

    # if the image has no faces
    if not image.has_faces():
        return response.ok({'message': 'No faces found'})  

    fullname = request.form.get('fullname')
    face_encoding = image.get_face_encodings()[0]
    # TODO: store image in S3 and return url
    face_id = db.add_face(fullname, face_encoding)

    data = {
            "face_id": face_id,
            "Person": fullname,
            "message": 'face add successfuly'
           }
    return response.created(data)




@app.route('/detect', methods=['POST'])
def detect_faces():
    # If the user did not provide an image
    if not ('image' in request.files):
        return response.bad_request("No image uploaded"), 400

    file = request.files.get('image')
    image = Image(file)

    face_found = image.has_faces()
    number_of_faces = image.number_of_faces()

    data = {
        'Detected': face_found,
        'Number_of_faces': number_of_faces
    }
    return response.ok(data), 200


@app.route('/compare', methods=['POST'])
def compare_two_faces():
    if not ('image1' in request.files) and ('image2' in request.files):
        return response.bad_request('Missing parameters (image1 or image2)'), 400


    file1 = request.files.get('image1')
    file2 = request.files.get('image2')
    image1 = Image(file1)
    image2 = Image(file2)

    # If one of the provided images has no faces
    if not (image1.has_faces() and image2.has_faces()):
        data = {
                "match": False,
                "message": "No faces detected"
               }
        return response.ok(data)

    encodings_1 = image1.get_face_encodings()
    encodings_2 = image2.get_face_encodings()

    match = False
    message = "No matching faces found on the images"
    for face in encodings_1:
        results = face_recognition.compare_faces(encodings_2, face)
        for result in results:
            if(result):
                match = True
                message = "Same face appears in both images"
    data = {
            "match": match,
            "message": message
           }
    return response.ok(data)





@app.route('/identify', methods=['POST'])
def identify_face():
    if not ('image' in request.files):
        return response.bad_request("No image uploaded"), 400

    file = request.files.get('image')
    image = Image(file)

    # If the provided image has no face
    if not (image.has_faces()):
        data = {
                  "match": False, 
                  "message": "No faces detected"
               }
        return response.ok(data), 200

    from_db = db.get_all_faces()

    # Take only the faces form the database
    encodings_from_db = []
    for arr in from_db:
        encodings_from_db.append(arr[2])

    face_encodings = image.get_face_encodings()

    for face in face_encodings:
        results = face_recognition.compare_faces(encodings_from_db, face)
        index = 0
        for result in results:
            if(result):
                data = {
                        'match': True,
                        'user_id': from_db[index]['user_id']
                        }
                return response.ok(data)
            index += 1

    return response.ok({"match": False, "user_id": "-1"})




app.run(host='0.0.0.0', port='5003', debug=True)


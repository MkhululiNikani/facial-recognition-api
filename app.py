from flask import Flask, request
import face_recognition
from image import Image
from database import Database
from response import Response
import pickle
import base64


app = Flask(__name__)

response = Response()
db = Database('127.0.0.1', 'nick', 'Gazorpazorp#2020', 'facial_recognition')


@app.route('/add-face', methods=['POST'])
def add_face():
    
  # check whether an image and a fullname are uploaded
    if not ('image' in request.files and 'fullname' in request.form):
        return response.bad_request('Missing parameters (image or fullname)')
  
  # If the uploaded file is an image
    try:
        file = request.files.get('image')
        image = Image(file)
    except IOError:
        return response.bad_request('Image file invalid')

  # If the image has faces in it [i.e it's not an image of a dog or a cat]
    if not image.has_faces():
        return response.request_failed('No faces found')  

  # Add face to the database
    fullname = request.form.get('fullname')
    face_encoding = image.get_face_encodings()[0] # If more than one face is detected only the first one will be used
    face_id = db.add_face(fullname, face_encoding)

    data = {
            "face_id": face_id,
            "Person": fullname,
            "message": 'Face Added Successfuly'
           }
    return response.created(data)


@app.route('/detect', methods=['POST'])
def detect_faces():

  # check whether the image was uploaded
    if not ('image' in request.files):
        return response.bad_request("No image uploaded")


  # If the uploaded file is an image
    try:
        file = request.files.get('image')
        image = Image(file)
    except IOError:
        return response.bad_request('Image file invalid')

 
    face_found = image.has_faces()
    number_of_faces = image.number_of_faces()

    data = {
        'Detected': face_found,
        'Number_of_faces': number_of_faces
    }
    return response.ok(data)


@app.route('/compare', methods=['POST'])
@app.route('/match', methods=['POST'])
def compare_two_faces():

  # check whether the two images were uploaded
    if not ('image1' in request.files) and ('image2' in request.files):
        return response.bad_request('Missing parameters (image1 or image2)')

   
  # If the uploaded files are not images
    try:
        file1 = request.files.get('image1')
        file2 = request.files.get('image2')
        image1 = Image(file1)
        image2 = Image(file2)
    except IOError:
        return response.bad_request('Image file invalid')


  # check whether the images have faces in them (not an image of a dog, cat or tree)
    if not (image1.has_faces() and image2.has_faces()):
        return response.ok([{"match": False, "message": "No faces found"}])

    encodings_1 = image1.get_face_encodings()
    encodings_2 = image2.get_face_encodings()

  # compare all face found on the first file with those found on the second
    for face_encoding in encodings_1:
        results = face_recognition.compare_faces(encodings_2, face_encoding)
        for result in results:
            if(result):
                return response.ok({"match": True, "message": "Match found"})

    return response.ok({"match": False, "message": "No Match found"})


@app.route('/identify', methods=['POST'])
def identify_face():

  # check whether the two images were uploaded
    if not ('image' in request.files):
        return response.bad_request("No image uploaded")


  # If the uploaded file is not images
    try:
        file = request.files.get('image')
        image = Image(file)
    except IOError:
        return response.bad_request('Image file invalid')
    

  # check whether the image has faces in it (not an image of a dog, cat or tree)
    if not (image.has_faces()):
        return response.ok({"match": False, "message": "No faces found"})

    db_records = db.get_all_faces()


  # take only the faces form the database not other attributes
  # base64 decode the faces
    encodings_from_db = []

    for arr in db_records:
        face = pickle.loads(base64.b64decode(arr[1]))
        encodings_from_db.append(face)


    face_encodings = image.get_face_encodings()

  # compare uploaded image to faces form the database
    for face in face_encodings:
        results = face_recognition.compare_faces(encodings_from_db, face)
        index = 0
        for result in results:
            if(result):
                data = {
                        'match': True,
                        'Fullname': db_records[index][0]
                        }
                return response.ok(data)
            index += 1

    return response.ok({"match": False})

app.run(host='0.0.0.0', port='5003', debug=True)

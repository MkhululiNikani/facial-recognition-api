from face_recognition import compare_faces

class Compare:

    def two_images(self, image1, image2):
        faces = image1.get_face_encodings()
        faces2 = image2.get_face_encodings()

        

    def face_to_face(self, face1, face2):
        return compare_faces([face1], face2)[0]

    def many_to_many(self, faces, faces2   ):
        for face in faces:
            results = compare_faces(faces2, face)
            for result in results:
                if(result):
                    return True
        return False
    
    def search_on_database(self, face):
        from_db = db.get_all_faces()
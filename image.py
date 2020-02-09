import face_recognition
class Image:

    def __init__(self, image_path):
        #Load image file into a numpy array ('face_recognition' likes it that way)
        self.image = face_recognition.load_image_file(image_path)

        self.face_encodings_list = None
        self.face_locations_list = None
        self.face_landmarks_list = None
 
   
    # Check whether any faces were detected
    def has_faces(self):
        return self.number_of_faces() > 0
    
    # Returns the number of faces detected
    def number_of_faces(self):
        return len(self.get_face_locations())

    # Returns face_locations in the image
    def get_face_locations(self):
        if(self.face_locations_list):
            return self.face_locations_list

        self.face_location_process()
        return self.face_locations_list

    # Returns a list of face_encodings for the detected faces
    def get_face_encodings(self):
        if(self.face_encodings_list):
            return self.face_encodings_list

        self.face_encoding_process()
        return self.face_encodings_list

    # Returns a list of landmarks positions of the detected faces
    def get_face_landmarks(self):
        # if(self.face_landmarks_list):
        #     return self.face_landmarks_list

        self.face_landmarks_process()
        return self.face_landmarks_list

    #Return image as a numpy array
    def get_numpy_image(self):
        return self.image

    #   PROCESS FUNCTIONS
    def face_encoding_process(self):
        try:
            self.face_encodings_list = face_recognition.face_encodings(self.image, self.get_face_locations())
        except IndexError:
            self.face_encodings_list = []

    def face_location_process(self):
        self.face_locations_list = face_recognition.face_locations(self.image)

    def face_landmarks_process(self):
        self.face_landmarks_list = face_recognition.face_landmarks(self.image)

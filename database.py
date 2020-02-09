import mysql.connector as mysql
from mysql.connector import errorcode
import base64
import pickle

class Database:

    def __init__(self, host, username, password, database):
        self.host = host
        self.username = username
        self.password = password
        self.database = database
        self.db_conn = None

    # TODO: delete tis method
    def delete_all(self):
        self.open_conn()
        cursor = self.db_conn.cursor()
        query = ("DELETE FROM faces")
        cursor.execute(query)
        self.db_conn.commit()
        cursor.close()
        self.close_conn()


    # Get user face (by user_id)
    def get_face(self, fullname):
        self.open_conn()
        cursor = self.db_conn.cursor()

        query = ("SELECT fullname, face_encoding FROM faces WHERE fullname = %s")
                   

        cursor.execute(query, (fullname,))
        face = cursor.fetchone()
        
        face['face_encoding'] = self.base64decode(face[1])
        cursor.close()
        self.close_conn()

        return face

    # Get all the faces in the database
    def get_all_faces(self):
        self.open_conn()
        cursor = self.db_conn.cursor()

        query = ("SELECT fullname, face_encoding FROM faces")
                    

        cursor.execute(query)
        faces = cursor.fetchall()

        decoded_faces = []

        index = 0
        while index < len(faces):
            decoded_faces.append(faces[index])

        cursor.close()
        self.close_conn()

        return decoded_faces

    # Add a face to the database
    def add_face(self, fullname, face_encoding):
        face_encoding = self.base64encode(face_encoding)

        self.open_conn()
        cursor = self.db_conn.cursor()

        add_face = ("INSERT INTO faces "
                    "(fullname, face_encoding) "
                    "VALUES (%s, %s)")

        
        face_data = (fullname, face_encoding)
 
        cursor.execute(add_face, face_data)
        face_id = cursor.lastrowid

        self.db_conn.commit()
        cursor.close()
        self.close_conn()

        return face_id



    # Opens a database connection
    def open_conn(self):
        try:
            self.db_conn = mysql.connect(user=self.username, password=self.password,
                                         host=self.host, database=self.database, 
                                         auth_plugin='mysql_native_password')
        except mysql.Error as error:
            if error.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("DB: Incorrect username or password")
            elif error.errno == errorcode.ER_BAD_DB_ERROR:
                print("DB: Database does not exist")
            else:
                print("DB: " + error)

    # Close a database connection
    def close_conn(self):
        if self.db_conn:
            self.db_conn.close()



    # Base64 encode face_encoding so they can be stored in the database
    def base64encode(self, face):
        return base64.b64encode(face.dumps())
    
    def base64decode(self, encoding):
        return pickle.loads(base64.b64decode(encoding))



    def storeOnS3(self, file):
        pass
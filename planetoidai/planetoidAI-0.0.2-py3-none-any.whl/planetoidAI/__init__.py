# importing the requests library
import requests

def test(number):
    print("This is first function")
    return number

class Planetoid:
    def __init__(self):
        """
        docstring
        """
        pass

    def get_objects_from_image(self, filename, threshold = 0.40):
        
        # api-endpoint
        URL = "https://planetoid.pythonanywhere.com/image"
        
        # sending get request and saving the response as response object
        files = {'image': open(filename,'rb')}
        values = {'threshold': threshold}
        
        response = requests.post(URL, files=files, data=values)

        # extracting data in json format
        data = response.json()
        
        return data

    def get_translation(self, input_text, translate_to = "gu"):
        
        # api-endpoint
        URL = "https://planetoid.pythonanywhere.com/translator"
        
        # sending get request and saving the response as response object
        values = {"text": input_text, "to": translate_to}
        
        response = requests.post(URL, json=values)
        
        # extracting data in json format
        data = response.json()
        
        return data

    def get_age_gender_from_image(self, filename, threshold = 0.40):
        
        # api-endpoint
        URL = "https://planetoids.pythonanywhere.com/faceimage"
        
        # sending get request and saving the response as response object
        files = {'image': open(filename,'rb')}
        values = {'threshold': threshold}
        
        response = requests.post(URL, files=files, data=values)

        # extracting data in json format
        data = response.json()
        
        return data

    def get_face_race_from_image(self, filename, threshold = 0.40):
        
        # api-endpoint
        URL = "https://planetoids.pythonanywhere.com/raceimage"
        
        # sending get request and saving the response as response object
        files = {'image': open(filename,'rb')}
        values = {'threshold': threshold}
        
        response = requests.post(URL, files=files, data=values)

        # extracting data in json format
        data = response.json()
        
        return data

    def get_face_location_from_image(self, filename, threshold = 0.40):
        # api-endpoint
        URL = "https://planetoids.pythonanywhere.com/face276"
        
        # sending get request and saving the response as response object
        files = {'image': open(filename,'rb')}
        values = {'threshold': threshold}
        
        response = requests.post(URL, files=files, data=values)

        # extracting data in json format
        data = response.json()
        
        return data

if __name__ == "__main__":
    pass
    # planetoid1 = Planetoid()

    # Get_objects_from_image
    # object_list = planetoid1.get_objects_from_image("../../HIMANSHU.jpeg")
    # print(object_list)

    # Get_translation
    # translation = planetoid1.get_translation("hello", translate_to='gu')
    # print(translation)

    # Get_age_gender_from_image
    # age_gender = planetoid1.get_age_gender_from_image("../../HIMANSHU.jpeg")
    # print(age_gender)

    # Get_face_race_from_image
    # nationality = planetoid1.get_face_race_from_image("../../HIMANSHU.jpeg")
    # print(nationality)

    # Get_face_location_from_image
    # face_276 = planetoid1.get_face_location_from_image( filename= "../../HIMANSHU.jpeg")
    # print(face_276)



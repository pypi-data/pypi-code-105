import os
import sys
import requests
import getpass

# URL = "http://localhost:5000"
URL = "shubbansal27.pythonanywhere.com"

endpoint1 = URL + "/authenticate_pipclient"
endpoint2 = URL + "/submit_code_pip_module"

def main():
    
    # curr_directory = os.path.dirname(os.path.abspath(__file__))
    # file_path = curr_directory + "/" + "test_code.py"
    n = len(sys.argv)
    if n != 3:
        print("Invalid parameters.\n Usecase:\n dsa_buddy --submit <file_path>\n")
        return 

    try:
        file_path = os.path.abspath(sys.argv[2])
    except:
        print("Invalid file path.. ")
        return


    flag = True
    print("Submitting code to DSA_Buddy. Please provide login details: ")
    while True:
        print("Email: ", end=' ')
        email = input()
        if len(email.split('@')) != 2:
            print('Please provide valid email.')
        else:
            break
        
    try:
        print("Password: ", end=' ')
        password = getpass.getpass()
        print('\nAuthenticating...')
    except Exception as error:
        print('some error occured in authentication.')
        flag = False
    

    if flag:
        values = {'user_email': email, 'password': password}
        r = requests.post(endpoint1, data=values)
        resp = r.json()
        print("RESPONSE : ", resp['status'])
        
        if resp['status'] == 'Question not selected':
            print('Please select question from the bot.')
        elif resp['status'] == "Confirmation Needed":
            print(resp['user_prompt'])
            print("Please confirm. Enter Y or N [default -  N] : ", end=' ')
            inp = input().lower().strip()
            if inp == 'y':
                files = {'file': open(file_path, 'rb')}
                values = {'user_email': email, 'password': password, 'question_id': resp['question_id'], 'question_title': resp['question_title']}
                r = requests.post(endpoint2, files=files, data=values)
                resp = r.json()
                print("RESPONSE : ", resp['status'])


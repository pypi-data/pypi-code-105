
def submit(func):
    def wrapper(*args, **kwargs):

        from inspect import getsource
        source_code = getsource(func)
        # print(source_code)
        
        ##execute function with test cases:  Future work
        # r = func(*args, **kwargs)
        
        ##if testcases >>> 100% Pass then only upload it to server
        __upload_code(source_code)

    return wrapper



def __upload_code(source_code):

    # URL = "http://localhost:5000"
    URL = "http://shubbansal27.pythonanywhere.com"

    endpoint1 = URL + "/authenticate_pipclient"
    endpoint2 = URL + "/submit_code_pip_module"

    import requests
    # import getpass
    import pwinput

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
        # print("Password: ", end=' ')
        # password = getpass.getpass()
        password = pwinput.pwinput()
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
                values = {'user_email': email, 'password': password, 'question_id': resp['question_id'], 'question_title': resp['question_title'], 'code':source_code}
                r = requests.post(endpoint2, data=values)
                resp = r.json()
                print("RESPONSE : ", resp['status'])



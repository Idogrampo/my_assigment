import sqlite3
import time
import sys
import requests
import json
from requests.auth import HTTPBasicAuth

#Global Veriables
user = "idogrampo@gmail.com"
token = "AKCp8hyZQ1Qmhi8LeCYRS9qnSX8dkTMNH95QvTGn1EHNbPvZchsLAT4uYwhosHBdnJmMnLwbG"

#User data are store in the "task" db, user has 3 login attempts
def login():
    max_tries = 3
    attempts = 0
    while attempts != max_tries:
        username = input("Please enter your username: ")
        password = input("Please enter your password: ")
        with sqlite3.connect("task.db") as db:
            cursor = db.cursor()
        find_user = ("SELECT * FROM users WHERE username = ? AND password = ?")
        cursor.execute(find_user, [(username), (password)])
        results = cursor.fetchall()
        
        #pring welcome and user's nickname
        if results:
            for i in results:
                print ("Welcome back "+i[2] + "!")
            break
        else:
            print("Error - Can't locate the your user, please check your credentials")
            attempts += 1
            if attempts == max_tries:
                print("Error - You've reached the maximum number of attempts.\nExiting the system.")
                time.sleep(1)
                sys.exit()

#serves "ping","status" and "storage" endpoints
def api_calls(endpoint):

        url = "https://idotask.jfrog.io/artifactory/api"
        response = requests.get(url + endpoint, auth=HTTPBasicAuth(user, token))
    
        #bytes to str 
        fixed_response = response.content.decode("UTF-8") 
        
        if endpoint == '/system/ping':
                print ("Server response: ",fixed_response)
                return
        #str to json
        json_response = json.loads(fixed_response)

        if endpoint == '/system/version':
                print (json_response["version"]) 
                return
                
        elif endpoint == '/storageinfo':
                #print formatted json
                print(json.dumps(json_response, indent=4, sort_keys=True))
                return


def create_user(username,user_json):

    url = f"https://idotask.jfrog.io/artifactory/api/security/users/{username}"
   
    response = requests.put(url, auth=HTTPBasicAuth(user, token),json=user_json)
    if (response.status_code) == 201:
            print ("Info - User was craeted succcessfuly")
    else:
            fixed_response = response.content.decode("UTF-8")
            print("Error - couldn't create user. Error message access::\n" + fixed_response +  "\nplease use the error message to fix it and try again")


def delete_user(username):

        #url + credentials for jfog platform
        url = f"https://idotask.jfrog.io/artifactory/api/security/users/{username}"
        user = "idogrampo@gmail.com"
        token = "AKCp8hyZQ1Qmhi8LeCYRS9qnSX8dkTMNH95QvTGn1EHNbPvZchsLAT4uYwhosHBdnJmMnLwbG"

        response = requests.delete(url, auth=HTTPBasicAuth(user, token))
        fixed_response = response.content.decode("UTF-8")        
        if (response.status_code) == 200:
                print (fixed_response)
        else:
                print("Error - couldn't delete user. Error message access::\n" + fixed_response +  "\nplease use the error message to fix it and try again")

#CLI menu
def menu():
    while True:
        print ("Please choose an action:")
        user_menu = ('''
                1 - System Ping
                2 - System Version
                3 - Create User
                4 - Delete User
                5 - Get Storage Info
                6 - Exit 
        ''')

        user_choice = input(user_menu)

        if user_choice == "1":
            api_calls(endpoint = "/system/ping")

        elif user_choice =="2":
            api_calls(endpoint = "/system/version")

        elif user_choice =="3":
            print('''
                Please enter the user informantion.
                password requirements:
                - At leaset 8 characters.
                - At least one uppercase and lowercase letters
                - At least one number or special character
            ''')
            username = input("enter username: ")
            email = input("enter email: ")
            password = input("enter password: ")
            user_string = '''{"name":"%s","email":"%s","password":"%s"}''' % (username,email,password)
            user_json = json.loads(user_string)
            create_user(username=username,user_json=user_json)

        elif user_choice == "4":
            username = input("Please enter the username that you want to delete: ")
            delete_user(username)

        elif user_choice == "5":
            api_calls(endpoint = "/storageinfo")

        elif user_choice == "6":
            print ("Exiting, see you later!")
            time.sleep(1)
            sys.exit()

        else:
            print ("Invalid input")

# ---Start---#

login()
menu()
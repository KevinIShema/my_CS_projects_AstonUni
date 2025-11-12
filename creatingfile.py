# this is the way of creating and writing files in python 


import re

users = {'alice': 'apassword', 'peter': 'ppassword', 'john': 'jpassword'}

with open('users.txt', 'w') as file:
    for username, password in users.items():
        file.write(f"{username}:{password}\n")
file.close()     



'''
here is the output of created file


alice:apassword
peter:ppassword
john:jpassword


'''
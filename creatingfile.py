# this is the way of creating and writing files in python 


# import re

# users = {'alice': 'apassword', 'peter': 'ppassword', 'john': 'jpassword'}

# with open('users.txt', 'w') as file:
#     for username, password in users.items():
#         file.write(f"{username}:{password}\n")
# file.close()     



'''
here is the output of created file


alice:apassword
peter:ppassword
john:jpassword


'''



import re

users = {}
numberofusers = int(input("how many users u want to add in to the file?: "))
for i in range (numberofusers):
    user = input("please enter your name ")
    pasword = input("please enter your pasword")

    users[user] = pasword

with open('users.txt', 'w') as file:
    for username, password in users.items():
        file.write(f"{username}:{password}\n")
file.close()     



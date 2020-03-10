from flask import request

def CheckIfLoggedIn(User):
    loggedIn = False
    tokenId = request.cookies.get('token')
    # Check if there is a token saved in cookie
    if tokenId != None:
        print(User.email)
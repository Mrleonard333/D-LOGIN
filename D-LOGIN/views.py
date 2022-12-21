from django.shortcuts import redirect
from django.shortcuts import render
from . import models

AC_Cookie = None # < Variable for account storage
Information = False # < Variable for Information storage
History = False # < Variable for all Information store

# Create your views here.

def HISTORY_MAKER(USER):
    global AC_Cookie, Information

    History = list()
    AC_Cookie = USER
    All = models.information.objects.filter(User=USER) # < Will return a list of the user's posts

    for H in All:
        History.append(str(H.Info)) # < Will create a list of information strings
    return History

def index(request):
    global AC_Cookie, History, Information

    try:
        B=str(request.POST["BUTTON"]) # < Will get the button pressed data
        History = HISTORY_MAKER(AC_Cookie)

        if B == "SING_UP":
            return redirect('/SING_UP/') # < Will redirect the user for the sing up page
        
        if B == "LOGIN":
            return redirect('/LOGIN/')

        if B == "DELETE":
            All = models.information.objects.filter(User=AC_Cookie) # < Will filter the posts of the user
            for A in All:
                A.delete() # < And delete it
            models.account.objects.get(Username=AC_Cookie).delete() # < Will delete the account

            History = False
            AC_Cookie = None

            return render(request, 'HOME.html', {"CK":AC_Cookie, "HY":History, "CHANGE_PASS":False}) # < Will show the page
                                                # ^ Dict with important variables
        if B == "CHANGE THE PASSWORD":
            return render(request, 'HOME.html', {"CK":AC_Cookie, "HY":History, "CHANGE_PASS":"CHANGING"})
        
        if B == "SEND":
            try:
                Password = str(request.POST["NEW_PASS"]).strip()
                
                if Password:
                    AC = models.account.objects.get(Username=AC_Cookie)
                    AC.Password = Password
                    AC.save() # < Will save the changes of the database
                    return render(request, 'HOME.html', {"CK":AC_Cookie, "HY":History, "CHANGE_PASS":"CHANGED"})
                else:
                    return render(request, 'HOME.html', {"CK":AC_Cookie, "HY":History, "CHANGE_PASS":"ERROR"})
            except:
                return render(request, 'HOME.html', {"CK":AC_Cookie, "HY":History, "CHANGE_PASS":"ERROR"})
        
        if B == "REGISTER":
            info = str(request.POST["INFO"]).strip()

            if not Information or Information != info and len(info) >= 1:
                Information = str(request.POST["INFO"]).strip()
                models.information(User=AC_Cookie, Info=Information).save()
            
            History = HISTORY_MAKER(AC_Cookie)
            return render(request, 'HOME.html', {"CK":AC_Cookie, "HY":History, "CHANGE_PASS":False})
    except:
        return render(request, 'HOME.html', {"CK":AC_Cookie, "HY":History, "CHANGE_PASS":False})

def SING_UP(request):
    global AC_Cookie, History

    try:
        B=str(request.POST["BUTTON"])

        if B == "EXIT":
            return redirect('/')

        if B == "SEND":
            ACCOUNT = True # < Variable that says if the account has been created
            Username = str(request.POST["Username"]).strip() # < Will get the username data
            Password = str(request.POST["Password"]).strip() # < Will get the password data
            US = models.account.objects.values_list('Username') # < Will get all the usernames from database

            if Password and Username:
                for U in US:       # v Will remove the white spaces
                    if Username == str(U[0]):
                        ACCOUNT = False
                        break
                if ACCOUNT:
                    History = HISTORY_MAKER(Username)
                    AC = models.account(Username=Username, Password=Password) # < Will create a new account
                    AC.save() # < Will save the new account on database
                
                return render(request, 'SING_UP.html', {"TRY":ACCOUNT, "CK":AC_Cookie})
            else:
                return render(request, 'SING_UP.html', {"TRY":"Null", "CK":AC_Cookie})
    except:
        return render(request, 'SING_UP.html', {"TRY":"NONE", "CK":AC_Cookie})

def LOGIN(request):
    global AC_Cookie, History

    try:
        B=str(request.POST["BUTTON"])

        if B == "EXIT":
            return redirect('/')
        if B == "SEND":
            ACCOUNT = False
            Username = str(request.POST["Username"]).strip()
            Password = str(request.POST["Password"]).strip()
            AC = models.account.objects.all() # < Will get all accounts

            if Password and Username:
                Login = f"{Username} {Password}"

                for A in AC:
                    if Login == str(A):
                        History = HISTORY_MAKER(Username)
                        ACCOUNT = True
                        break

                return render(request, 'LOGIN.html', {"TRY":ACCOUNT, "CK":AC_Cookie})
            else:
                return render(request, 'LOGIN.html', {"TRY":"Null", "CK":AC_Cookie})
    except:
        return render(request, 'LOGIN.html', {"TRY":"NONE", "CK":AC_Cookie})

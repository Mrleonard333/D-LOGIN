from django.shortcuts import redirect
from django.shortcuts import render
from . import models

Account_Cookie = None # < Variable for account storage
Information = False # < Variable for Information storage
History = False # < Variable for all Information store

# Create your views here.

def HISTORY_MAKER(USER):
    global Account_Cookie, Information

    History = list()
    Account_Cookie = USER
    Posts = models.information.objects.filter(User=USER) # < Will return a list of the user's posts

    for PS in Posts:
        History.append(str(PS.Info)) # < Will create a list of information strings
    return History

def index(request):
    global Account_Cookie, History, Information

    try:
        Button=str(request.POST["BUTTON"]) # < Will get the button pressed data
        History = HISTORY_MAKER(Account_Cookie)

        if Button == "SING_UP":
            return redirect('/SING_UP/')
        
        if Button == "LOGIN":
            return redirect('/LOGIN/')

        if Button == "DELETE":
            User_Posts = models.information.objects.filter(User=Account_Cookie) # < Will filter the posts of the user
            for UP in User_Posts:
                UP.delete()
            models.account.objects.get(Username=Account_Cookie).delete() # < Will delete the account

            History = False
            Account_Cookie = None

            return render(request, 'HOME.html', {"AC":Account_Cookie, "HY":History, "CHANGE_PASS":False}) # < Will show the page
                                                # ^ Dict with important variables
        if Button == "CHANGE THE PASSWORD":
            return render(request, 'HOME.html', {"AC":Account_Cookie, "HY":History, "CHANGE_PASS":"CHANGING"})
        
        if Button == "SEND":
            try:                                        # v Will remove white spaces
                Password = str(request.POST["NEW_PASS"]).strip()
                
                if Password:
                    Account = models.account.objects.get(Username=Account_Cookie)
                    Account.Password = Password
                    Account.save() # < Will save the changes of the database
                    return render(request, 'HOME.html', {"AC":Account_Cookie, "HY":History, "CHANGE_PASS":"CHANGED"})
                else:
                    return render(request, 'HOME.html', {"AC":Account_Cookie, "HY":History, "CHANGE_PASS":"ERROR"})
            except:
                return render(request, 'HOME.html', {"AC":Account_Cookie, "HY":History, "CHANGE_PASS":"ERROR"})
        
        if Button == "REGISTER":
            info = str(request.POST["INFO"]).strip()

            if not Information or Information != info and len(info) >= 1:
                Information = str(request.POST["INFO"]).strip()
                models.information(User=Account_Cookie, Info=Information).save()
            
            History = HISTORY_MAKER(Account_Cookie)
            return render(request, 'HOME.html', {"AC":Account_Cookie, "HY":History, "CHANGE_PASS":False})
    except:
        return render(request, 'HOME.html', {"AC":Account_Cookie, "HY":History, "CHANGE_PASS":False})

def SING_UP(request):
    global Account_Cookie, History

    try:
        Button=str(request.POST["BUTTON"])

        if Button == "EXIT":
            return redirect('/')

        if Button == "SEND":
            AT_Verify = True # < Variable that says if the account has been created
            Username = str(request.POST["Username"]).strip() # < Will get the username data
            Password = str(request.POST["Password"]).strip() # < Will get the password data
            DB_Usernames = models.account.objects.values_list('Username') # < Will get all the usernames from database

            if Password and Username:
                for User in DB_Usernames:
                    if Username == str(User[0]):
                        AT_Verify = False
                        break
                if AT_Verify:
                    History = HISTORY_MAKER(Username)
                    New_Account = models.account(Username=Username, Password=Password) # < Will create a new account
                    New_Account.save() # < Will save the new account on database
                
                return render(request, 'SING_UP.html', {"TRY":AT_Verify, "AC":Account_Cookie})
            else:
                return render(request, 'SING_UP.html', {"TRY":"Null", "AC":Account_Cookie})
    except:
        return render(request, 'SING_UP.html', {"TRY":"NONE", "AC":Account_Cookie})

def LOGIN(request):
    global Account_Cookie, History

    try:
        Button=str(request.POST["BUTTON"])

        if Button == "EXIT":
            return redirect('/')
        if Button == "SEND":
            AT_Verify = False
            Username = str(request.POST["Username"]).strip()
            Password = str(request.POST["Password"]).strip()
            Account = models.account.objects.all() # < Will get all accounts

            if Password and Username:
                Login = f"{Username} {Password}"

                for AT in Account:
                    if Login == str(AT):
                        History = HISTORY_MAKER(Username)
                        AT_Verify = True
                        break

                return render(request, 'LOGIN.html', {"TRY":AT_Verify, "AC":Account_Cookie})
            else:
                return render(request, 'LOGIN.html', {"TRY":"Null", "AC":Account_Cookie})
    except:
        return render(request, 'LOGIN.html', {"TRY":"NONE", "AC":Account_Cookie})

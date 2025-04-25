from flask import Flask,render_template,request,redirect
import sqlite3

app=Flask(__name__)


activeUser=0

@app.route('/')
#def index():
    #return render_template('login.html')

#activeUser=0

def loginCheck():#For checking that a user is viewing with an account
    activeUserCheck=activeUser
    if activeUserCheck==0:
        return redirect('/login')
    else:
        return redirect('/itemSearch')
        #returns as string so other functions can use to connect to specific table



@app.route('/login',methods=["GET","POST"],)
def Login():
    if request.method=="POST":
        if "submitButton" in request.form:
            userNameInp=request.form.get("userName")#pulls info from submit
            passwordInp=request.form.get("password")

            if userNameInp=="":
                return redirect('/')

            userSplit=list(userNameInp)#converts userID into database table name
            userID=1
            tempList=[]
            for i in range(len(userSplit)-2):
                temp=userSplit[i]
                temp=temp.upper()
                tempNum=ord(temp)-64#turns into num up to 26 for calculation
                tempList.append(tempNum)
            tempList.append(int(userSplit[4]))#done seperate as couldnt change from negative after orb()
            tempList.append(int(userSplit[5]))

            for i in range(len(tempList)):
                userID=userID*tempList[i]#gets a single number from temp list

            connection=sqlite3.connect('./Database/User.db')
            cursor=connection.cursor()
            searchPass="""SELECT Password FROM [%s]"""%int(userID)

            try:
                cursor.execute(searchPass)
                passwordfetch=cursor.fetchall()
                connection.commit()
                connection.close()#fetches password from specific database
                password=''.join(str(passwordfetch))
                password=password.replace("[('","")
                password=password.replace("',)]","")#strips password to same format as input

                loginOutcome="False"
                if password==passwordInp:
                    global activeUser
                    activeUser=int(userID)#sets active user as logged in user
                    return redirect('/itemSearch')#logs in user
                else:
                    loginOutcome=False
                return redirect('/login')#restarts if false
            
            except sqlite3.OperationalError:#for if table in db doesnt exist or error
                connection.close()
                return redirect('/login')
        elif "signUp" in request.form:
            return redirect('/signUp')
    return render_template('login.html')


@app.route('/signUp',methods=["GET","POST"],)
def signUp():
    if request.method=="POST":
        if "submitButton" in request.form:
            forename=request.form.get("forename")
            surname=request.form.get("surname")
            email=request.form.get("email")
            password=request.form.get("password")
            phoneNum=request.form.get("number")
            age=request.form.get("age")
            postCode=request.form.get("postcode")
            #below are need to be change later
            mainLib="0"
            address="N/A"
            itemID=0
            if (forename!="" and surname!="" and email!="" and password!="" and phoneNum!="" and age!="" and postCode!=""):
                connection=sqlite3.connect('./Database/User.db')
                cursor=connection.cursor()
                for i in range(26*26*26*26*9*9):#checks to see if it can pull a userID up to max amount of accounts
                    tableCount="""SELECT UserID FROM [%s]"""%str(i+1)#checks each to allow for account deletion
                    try:
                        cursor.execute(tableCount)
                    except:
                        newUserID=i+1#adds one to amount counted and stops the loop
                        break

                newUserTable="""CREATE TABLE IF NOT EXISTS [%s](
                UserID VARCHAR,
                Privilege CHAR,
                Forename CHAR,
                Surname CHAR,
                Email VARCHAR,
                PhoneNumber CHAR,
                Password VARCHAR,
                Age INT,
                Address VARCHAR,
                Postcode VARCHAR,
                MainLib INT,
                Item1ID INT,
                Item2ID INT,
                Item3ID INT
                );"""%newUserID
                cursor.execute(newUserTable)
                cursor.execute("""INSERT INTO [%s] (UserID,Privilege,Forename,Surname,Email,PhoneNumber,Password,Age,Address,Postcode,MainLib,Item1ID,Item2ID,Item3ID)
                            values(?,?,?,?,?,?,?,?,?,?,?,?,?,?)"""%newUserID,(newUserID,"customer",forename,surname,email,phoneNum,password,age,address,postCode,mainLib,itemID,itemID,itemID))
                connection.commit()
                connection.close()
                return redirect('/login')
            else:
                return redirect('/signUp')

        elif "login" in request.form:
            return redirect('/login')
    return render_template('SignUp.html')


@app.route('/itemSearch',methods=["GET","POST"],)
def itemSearch():
    headings=('','','','','','')
    data=[
        ("","","","","","")
    ]
    if request.method=="POST":
        if "searchItem" in request.form:
            inputSearch=request.form.get("Search")
            if inputSearch=="":
                print
            else:
                conItem=sqlite3.connect('./Database/items.db')
                curItem=conItem.cursor()
                itemIDRequest="""SELECT ItemID FROM ITEMS WHERE ItemName=='[%s]'"""%inputSearch
                curItem.execute(itemIDRequest)
                itemID=str(curItem.fetchall())
                itemID=itemID.replace('[(','')
                itemID=itemID.replace(',)]','')
                conItem.commit()
                conItem.close()

                conUser=sqlite3.connect('./Database/User.db')
                curUser=conUser.cursor()
                mainLibSearch="""SELECT MainLib FROM [%s]"""%str(activeUser)
                curUser.execute(mainLibSearch)
                mainLib=str(curUser.fetchall())
                mainLib=mainLib.replace('[(','')
                mainLib=mainLib.replace(',)]','')
                conUser.commit()
                conUser.close()#pulls the users mainLib(temp set to 10 for testing)


                conLib=sqlite3.connect('./Database/Library.db')
                curLib=conLib.cursor()
                stockCheck="""SELECT ItemID FROM [%s] WHERE UserID==0"""%mainLib#pulls all records of items if in table
                curLib.execute(stockCheck)
                emptyItem=curLib.fetchall()
                conLib.commit()
                conLib.close()

                result=[]
                conItem=sqlite3.connect('./Database/items.db')
                curItem=conItem.cursor()
                for i in range(len(emptyItem)):#cycles through all possible items with no users
                    test=str(emptyItem[i])
                    test=test.replace('(','')
                    test=test.replace(',)','')
                    itemDescriptor="""SELECT * FROM ITEMS WHERE ItemID=="""+test#needs to be added as a string after in this fashion or crash
                    curItem.execute(itemDescriptor)
                    itemInfo=curItem.fetchall()
                    result.append(itemInfo)#makes list of all descriptors
                conItem.commit()
                conItem.close()

                headings=('Name','Author','Type','Blurb','Word Count','Availability')
                data=[]
                for x in range(len(result)):
                    tempResult=[]
                    tempResult=str(result[x]).split(',')
                    tempResult.pop(0)
                    tempResult.pop()
                    data.append(tempResult)
                return render_template('itemSearch.html',headings=headings,data=data)
            
        elif "takeOut" in request.form:#for aquiring items
            conUser=sqlite3.connect('./Database/User.db')
            curUser=conUser.cursor()
            curUser.execute("""SELECT Item1ID FROM [%s];"""%activeUser)
            item1=curUser.fetchone()
            curUser.execute("""SELECT Item2ID FROM [%s];"""%activeUser)
            item2=curUser.fetchone()
            curUser.execute("""SELECT Item3ID FROM [%s];"""%activeUser)
            item3=curUser.fetchone()
            
            return data[0]

            userItems=[item1,item2,item3]
            itemIDList=["Item1ID","Item2ID","Item3ID"]
            for i in range(len(userItems)):
                if userItems[i]=="0":
                    query="""UPDATE [%s] SET (?)='0'"""%activeUser,(itemIDList[0])#replace 0 with book in table
                    curUser.execute(query)
                else:
                    itemIDList.pop()
            
            conUser.commit()
            conUser.close()
            return render_template('/itemSearch')

        elif "currBooks" in request.form:
            return redirect('/home')

        elif "logout" in request.form:
            return redirect('/logout')
    return render_template('itemSearch.html',headings=headings,data=data)

@app.route('/home',methods=["GET","POST"],)
def items():
    headings=('Item Name')
    conUser=sqlite3.connect('./Database/User.db')#pulls each book currently have taken out
    curUser=conUser.cursor()
    curUser.execute("""SELECT Item1ID FROM [%s];"""%activeUser)
    item1=curUser.fetchone()
    curUser.execute("""SELECT Item2ID FROM [%s];"""%activeUser)
    item2=curUser.fetchone()
    curUser.execute("""SELECT Item3ID FROM [%s];"""%activeUser)
    item3=curUser.fetchone()
    userItems=[item1,item2,item3]
    conUser.commit()
    conUser.close()

    for x in range(len(userItems)):
        bracket=str(userItems[x])
        bracket=bracket.replace('(','')
        bracket=bracket.replace(',)','')
        userItems[x]=bracket#cycles through items and removes brackets as tuples cannot be passed in next section

    conItems=sqlite3.connect('./Database/items.db')
    curItems=conItems.cursor()    
    temp=', '.join('?' for _ in userItems)#automatically sets up ? at once
    query=f"SELECT ItemName FROM ITEMS WHERE ItemID IN({temp})"
    curItems.execute(query,userItems)
    results=curItems.fetchall()
    curItems.close()


    if request.method=="POST":#needs to be after set table as that needs to be base feature
        if "searchItem" in request.form:
            return redirect('/itemSearch')#switches back to main page
    
    elif "return" in request.form:#for returing items
            conUser=sqlite3.connect('./Database/User.db')
            curUser=conUser.cursor()
            curUser.execute("""SELECT Item1ID FROM [%s];"""%activeUser)
            item1=curUser.fetchone()
            curUser.execute("""SELECT Item2ID FROM [%s];"""%activeUser)
            item2=curUser.fetchone()
            curUser.execute("""SELECT Item3ID FROM [%s];"""%activeUser)
            item3=curUser.fetchone()
            
            userLib=curUser.execute("SELECT MainLib FROM [%s];")
            conItem=sqlite3.connect('./Database/items.db')
            curItem=conItem.cursor()
            curItem.execute("""UPDATE ? SET UserID='0' WHERE ItemID=?"""),(userLib,item1)
            curItem.commit()
            curItem.close()
            
            curUser.execute("""UPDATE ? SET Item1ID=?"""),(activeUser,item2)
            curUser.execute("""UPDATE ? SET Item2ID=?"""),(activeUser,item3)
            curUser.execute("""UPDATE [%s] SET Item3ID='0'""")%activeUser

            conUser.commit()
            conUser.close()
    return render_template('home.html',headings=headings, data=results)

@app.route('/logout',methods=["GET","POST"],)
def logout():
    global activeUser
    activeUser=0
    return redirect('/login')

if __name__=="__main__":
    app.run(debug=True)
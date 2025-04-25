import sqlite3
import random as rand

#Items Creation
connection=sqlite3.connect('items.db')

cursor=connection.cursor()

ItemTable="""CREATE TABLE IF NOT EXISTS ITEMS(
ItemID INT NOT NULL,
ItemName VARCHAR(255) NOT NULL,
Author CHAR(25) NOT NULL,
Type CHAR(25) NOT NULL,
Blurb VARCHAR,
NumWords INT,
NumInSystem INT
);"""

cursor.execute(ItemTable)
print("Items added")

#item database fill
NumOfItems=1000
for i in range(NumOfItems):
    itemName=str(i)
    author=str(i)+"Gregg"
    type="book"
    blurb=str(i*i)+str(i*i)
    words=i*i
    systemNum=i+i
    cursor.execute("INSERT INTO ITEMS (ItemID,ItemName,Author,Type,Blurb,NumWords,NumInSystem) VALUES (?,?,?,?,?,?,?)",((i+1),itemName,author,type,blurb,words,systemNum))
    connection.commit()
print("Items filled")

connection.close()


#Library creation
connection=sqlite3.connect('Library.db')

cursor=connection.cursor()

IDtable="""CREATE TABLE IF NOT EXISTS LIB_ID(
LibID INT,
LibName VARCHAR,
Location VARCHAR,
OpenTime INT,
CloseTime INT,
NumOfItems INT
);"""

libList=[]
testLib=5#change for amount of Individual libraries wanted
for i in range(testLib):
    libList.append(i+1)
    i=+1
for j in range(len(libList)):
    libID=str(libList[j])
    libTable="CREATE TABLE IF NOT EXISTS [%s] (LibID INT,ItemID INT,UserID);"%libID
    cursor.execute(libTable)

cursor.execute(IDtable)
print("IDtable added")

#Library databases fill
for x in range(len(libList)):
    libID=str(libList[x])
    libName="South_Yorkshire"+str(x+1)
    location="sheffield"
    openTime=8
    closeTime=8
    numOfItems=(x+1)*350
    if numOfItems>1000:
        numOfItems=numOfItems/7

    randomItem=rand.randint(1,1000)
    tempRandUser=rand.randint(1,2106)

    cursor.execute("INSERT INTO [%s] (LibID,ItemID,UserID) VALUES (?,?,?)"%libID,(libID,randomItem,tempRandUser))
    cursor.execute("INSERT INTO [%s] (LibID,ItemID,UserID) VALUES (?,?,?)"%libID,(libID,randomItem,0))#test data for unclaimed item
    cursor.execute("INSERT INTO LIB_ID(LibID,LibName,Location,OpenTime,CloseTime,NumOfItems) VALUES (?,?,?,?,?,?)",(libList[x],libName,location,openTime,closeTime,numOfItems))
    connection.commit()

connection.close()


#user creation
connection=sqlite3.connect('User.db')

cursor=connection.cursor()

userList=[]
testRange=2106#change number for database creation
for i in range(testRange):
    userList.append(i+1)
for j in range(len(userList)):
    userID=str(userList[j])
    userTable="""CREATE TABLE IF NOT EXISTS [%s](
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
    );"""%userID
    cursor.execute(userTable)

    privilege="admin"
    if j>100:
        privilege="customer"
    forename=userID+"Andrew"
    surname="Befumo"+userID
    email="User"+userID+"@email.com"
    phoneNumber="0800118118"
    password="password"+userID
    age=42
    address="10 Downing Street"
    postCode="SW1A2AA"
    mainLib=3
    item1=rand.randint(1,1000)
    item2=rand.randint(1,1000)
    item3=rand.randint(1,1000)

    cursor.execute("""INSERT INTO [%s] (UserID,Privilege,Forename,Surname,Email,PhoneNumber,Password,Age,Address,Postcode,MainLib,Item1ID,Item2ID,Item3ID)
                    values(?,?,?,?,?,?,?,?,?,?,?,?,?,?)"""%userID,(userID,privilege,forename,surname,email,phoneNumber,password,age,address,postCode,mainLib,item1,item2,item3))
    connection.commit()

print("user added")


connection.close()
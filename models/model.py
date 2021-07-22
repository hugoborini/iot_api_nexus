import json
import os 
import mysql.connector
import datetime

from influxdb_client import InfluxDBClient



def connectInlfux():
  client = InfluxDBClient(url="http://18.116.89.239:8086/", token="jIrsd7-eMaIwRxXI8FnnkeUGCAV7khgQJj3Gk6zVV51dDhB6Q0xM-2jPwM7iZpmOs7OI4lLjWV_1MZU1ouRgDA==", org="nexusproject")
  return client

def getNBpers():
  client = connectInlfux()
  returnData= {}
  query_api = client.query_api()

  query = """from(bucket: "mqttnexus")
    |> range(start: -2m)
    |> filter(fn: (r) => r["source_address"] == "12345678" or r["source_address"] == "13960537" or r["source_address"] == "22361595" or r["source_address"] == "24114793" or r["source_address"] == "51488201" or r["source_address"] == "54158491" or r["source_address"] == "58381714" or r["source_address"] == "60052006" or r["source_address"] == "62061965" or r["source_address"] == "68191831" or r["source_address"] == "69607072" or r["source_address"] == "73214383" or r["source_address"] == "7654321" or r["source_address"] == "94981317" or r["source_address"] == "987654543")
    |> filter(fn: (r) => r["_field"] == "data_value")
    |> filter(fn: (r) => r["_measurement"] == "NbPers" or r["_measurement"] == "Temperature")
    |> filter(fn: (r) => r["topic"] == "WEB2-GROUPE1/12345678/112" or r["topic"] == "WEB2-GROUPE1/12345678/122" or r["topic"] == "WEB2-GROUPE1/13960537/112" or r["topic"] == "WEB2-GROUPE1/13960537/122" or r["topic"] == "WEB2-GROUPE1/22361595/112" or r["topic"] == "WEB2-GROUPE1/22361595/122" or r["topic"] == "WEB2-GROUPE1/24114793/112" or r["topic"] == "WEB2-GROUPE1/24114793/122" or r["topic"] == "WEB2-GROUPE1/51488201/112" or r["topic"] == "WEB2-GROUPE1/51488201/122" or r["topic"] == "WEB2-GROUPE1/54158491/112" or r["topic"] == "WEB2-GROUPE1/54158491/122" or r["topic"] == "WEB2-GROUPE1/58381714/112" or r["topic"] == "WEB2-GROUPE1/58381714/122" or r["topic"] == "WEB2-GROUPE1/60052006/112" or r["topic"] == "WEB2-GROUPE1/60052006/122" or r["topic"] == "WEB2-GROUPE1/62061965/112" or r["topic"] == "WEB2-GROUPE1/62061965/122" or r["topic"] == "WEB2-GROUPE1/68191831/112" or r["topic"] == "WEB2-GROUPE1/68191831/122" or r["topic"] == "WEB2-GROUPE1/69607072/112" or r["topic"] == "WEB2-GROUPE1/69607072/122" or r["topic"] == "WEB2-GROUPE1/73214383/112" or r["topic"] == "WEB2-GROUPE1/73214383/122" or r["topic"] == "WEB2-GROUPE1/7654321/112" or r["topic"] == "WEB2-GROUPE1/7654321/122" or r["topic"] == "WEB2-GROUPE1/94981317/112" or r["topic"] == "WEB2-GROUPE1/94981317/122" or r["topic"] == "WEB2-GROUPE1/987654543/112" or r["topic"] == "WEB2-GROUPE1/987654543/122")
    |> yield(name: "mean")"""


  result = client.query_api().query(org="nexusproject", query=query)

  results = []
  for table in result:
      for record in table.records:
          results.append((record.get_value(), record.get_field(), record.get_measurement(), record.values.get("source_address")))

  for data in results:

    if data[2] == "NbPers":
      returnData[str(data[3])] = { "NbPers" : int(data[0])}
    
    if data[2] == "Temperature":
      returnData[str(data[3])]["Temperature"] = int(data[0])

  return returnData


def datetime_handler(x):
    if isinstance(x, datetime.datetime):
        return x.isoformat()
    raise TypeError("Unknown type")


def getIdRoomBYRoomName(nameRoom):
    bdd = connectBdd()
    
    mycursor = bdd.cursor(prepared=True)
    
    stmt = """SELECT id_room FROM room WHERE nameRoom = %s"""
    
    mycursor.execute(stmt, (nameRoom,))
    
    id_room = [{mycursor.description[index][0]:column for index, column in enumerate(value)} for value in mycursor.fetchall()]
    
    return id_room[0]['id_room']
    
def range_overlapping(x, y):
    if x.start == x.stop or y.start == y.stop:
        return False
    return x.start < y.stop and y.start < x.stop

def connectBdd():
    config = {
    'user': 'rklxk7ds9ab108ng',
    'password': 'relrb6leomiux08k',
    'port': 3306,
    'host': 'c8u4r7fp8i8qaniw.chr7pe7iynqr.eu-west-1.rds.amazonaws.com',
    'database': 'je3w8f0ftg7dcitn',
    }

    cnx = mysql.connector.connect(**config)

    return cnx

def isNotBook(nameSalle, start, end):
     #get data
    bdd = connectBdd()
    date = datetime.datetime.now()
    date = date.strftime("%Y-%m-%d")
    mycursor = bdd.cursor(prepared=True)
    
    stmt = """SELECT * FROM room INNER JOIN booking ON room.id_room = booking.id_room WHERE room.nameRoom = %s and booking.date = %s"""

    mycursor.execute(stmt, (nameSalle,date))

    columns = mycursor.description 

    allReservation = [{columns[index][0]:column for index, column in enumerate(value)} for value in mycursor.fetchall()]

    bdd.close()

    

    for i in range(len(allReservation)):
        isOverlap = range_overlapping(range(allReservation[i]["start"], allReservation[i]["end"]), range(int(start), int(end)))
        if isOverlap:
            return False

        
    return True

    

def getJson():
    now = datetime.datetime.now()
    date = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d")
    actualHour = now.hour
    bdd = connectBdd()

    influxData = getNBpers()
    print(influxData)
    
    
    mycursor = bdd.cursor(prepared=True)

    mycursor.execute("SELECT * FROM room") 

    Allrooms = [{mycursor.description [index][0]:column for index, column in enumerate(value)} for value in mycursor.fetchall()]

    for i in range(len(Allrooms)):

        stmt = "SELECT * FROM room INNER JOIN booking ON room.id_room = booking.id_room WHERE room.id_room = %s"
        mycursor.execute(stmt, (Allrooms[i]["id_room"],))
        roomInfo = [{mycursor.description [index][0]:column for index, column in enumerate(value)} for value in mycursor.fetchall()]

        #Allrooms[i]["nbPlaceTotal"] = Allrooms[i]["nbPlace"]

        if Allrooms[i]["freeAccess"] == 1:
            Allrooms[i]["freeAccess"] = True
        else:
            Allrooms[i]["freeAccess"] = False
        if Allrooms[i]["nbPlace"] - influxData[str(Allrooms[i]["nodeID"])]["NbPers"] < 0:
            Allrooms[i]["isFull"] = True
            Allrooms[i]["nbPlaceTotal"] = 0
        else :
            Allrooms[i]["nbPlaceTotal"] = Allrooms[i]["nbPlace"] - influxData[str(Allrooms[i]["nodeID"])]["NbPers"]
            Allrooms[i]["isFull"] = False
        
        Allrooms[i]["Temperature"] = influxData[str(Allrooms[i]["nodeID"])]["Temperature"]
        
        if(len(roomInfo) > 0):
            for y in range(len(roomInfo)):

                if str(roomInfo[y]["date"]) == date:
                    if roomInfo[y]["start"] <= actualHour <= roomInfo[y]["end"]:
                        Allrooms[i]["isBooked"] = True
                    else:
                        Allrooms[i]["isBooked"] = False
                else:
                    Allrooms[i]["isBooked"] = False


        else:
            Allrooms[i]["isBooked"] = False

    bdd.close()
    return Allrooms


def bookARoom(nameSalle, start, end, studentMail):

    if isNotBook(nameSalle, start, end):

        now = datetime.datetime.now()
        date = now.strftime("%Y-%m-%d")
        

        bdd = connectBdd()

        mycursor = bdd.cursor(prepared=True)

        stmt = """INSERT INTO booking(id_room, start, end, studentEmail, date) VALUES(%s,%s,%s,%s,%s)"""

        mycursor.execute(stmt, (getIdRoomBYRoomName(nameSalle),start, end, studentMail, date)) 

        bdd.commit()

        bdd.close()

        return mycursor.rowcount, "record(s) affected"
    else:
        return "room already booked"

def getBookingOfARoom(nameRoom):
    bdd = connectBdd()

    mycursor = bdd.cursor(prepared=True)

    stmt = """SELECT room.id_room, room.nameRoom, room.nbPlace, room.building, booking.id_booking, booking.start, booking.end, booking.studentEmail
            FROM room 
            INNER JOIN booking ON room.id_room = booking.id_room WHERE room.id_room = %s"""
    
    mycursor.execute(stmt, (getIdRoomBYRoomName(nameRoom),))
    
    roomInfo = [{mycursor.description [index][0]:column for index, column in enumerate(value)} for value in mycursor.fetchall()]
    
    bdd.close()
    print(roomInfo)
    if len(roomInfo) == 0:
        return ["oui"]

    return roomInfo

def removeABookingModel(id_booking):
    bdd = connectBdd()

    mycursor = bdd.cursor(prepared=True)

    stmt = "DELETE FROM booking WHERE id_booking = %s"

    mycursor.execute(stmt, (id_booking,))

    bdd.commit()

    bdd.close()

    return mycursor.rowcount, "record(s) deleted"

def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3

def getBookingDetailByRoomModel(room_id, rangeHour):
    
    bdd = connectBdd()
    intersectionTab2d = []
    bookingTab = {}
    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d")

    mycursor = bdd.cursor(prepared=True)

    stmt = """SELECT * FROM room INNER JOIN booking ON room.id_room = booking.id_room WHERE room.id_room = %s AND DATE = %s"""

    mycursor.execute(stmt, (room_id, date))

    allBooking = [{mycursor.description[index][0]:column for index, column in enumerate(value)} for value in mycursor.fetchall()]
    bdd.close()


    i = 0 
    for booking in allBooking:
        print(i)
        intersectionTab2d.insert(i,intersection(list(rangeHour), list(range(int(booking["start"]),int(booking["end"] + 1)))))
        i = i + 1

    print(intersectionTab2d)

    for i in rangeHour:
        bookingTab[str(i)] = False
    
    for intersectionTab in intersectionTab2d:
        for i in intersectionTab:
            bookingTab[str(i)] = True
    
    return bookingTab

def getBookingByEmailModel(email):
    bdd = connectBdd()
    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d")
    mycursor = bdd.cursor(prepared=True)


    stmt = """SELECT room.id_room, room.nameRoom, room.nbPlace, room.building, booking.id_booking, 
                    booking.start, booking.end, booking.studentEmail
                FROM room INNER JOIN booking ON room.id_room = booking.id_room WHERE booking.studentEmail = %s AND DATE = %s"""

    mycursor.execute(stmt, (email, date))
    
    allBooking = [{mycursor.description[index][0]:column for index, column in enumerate(value)} for value in mycursor.fetchall()]
    
    bdd.commit()

    print(allBooking)
    return allBooking

def getInfoOfARoomBYIdRoom(idRoom):
    now = datetime.datetime.now()
    date = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d")
    actualHour = now.hour
    bdd = connectBdd()

    influxData = getNBpers()
    print(influxData)
    
    
    mycursor = bdd.cursor(prepared=True)

    mycursor.execute("SELECT * FROM room WHERE id_room = %s", (idRoom,)) 

    Allrooms = [{mycursor.description [index][0]:column for index, column in enumerate(value)} for value in mycursor.fetchall()]

    for i in range(len(Allrooms)):

        stmt = "SELECT * FROM room INNER JOIN booking ON room.id_room = booking.id_room WHERE room.id_room = %s"
        mycursor.execute(stmt, (Allrooms[i]["id_room"],))
        roomInfo = [{mycursor.description [index][0]:column for index, column in enumerate(value)} for value in mycursor.fetchall()]

        #Allrooms[i]["nbPlaceTotal"] = Allrooms[i]["nbPlace"]

        if Allrooms[i]["freeAccess"] == 1:
            Allrooms[i]["freeAccess"] = True
        else:
            Allrooms[i]["freeAccess"] = False
        if Allrooms[i]["nbPlace"] - influxData[str(Allrooms[i]["nodeID"])]["NbPers"] < 0:
            Allrooms[i]["isFull"] = True
            Allrooms[i]["nbPlaceTotal"] = 0
        else :
            Allrooms[i]["nbPlaceTotal"] = Allrooms[i]["nbPlace"] - influxData[str(Allrooms[i]["nodeID"])]["NbPers"]
            Allrooms[i]["isFull"] = False
        
        Allrooms[i]["Temperature"] = influxData[str(Allrooms[i]["nodeID"])]["Temperature"]
        
        if(len(roomInfo) > 0):
            for y in range(len(roomInfo)):

                if str(roomInfo[y]["date"]) == date:
                    if roomInfo[y]["start"] <= actualHour <= roomInfo[y]["end"]:
                        Allrooms[i]["isBooked"] = True
                    else:
                        Allrooms[i]["isBooked"] = False
                else:
                    Allrooms[i]["isBooked"] = False


        else:
            Allrooms[i]["isBooked"] = False

    bdd.close()
    return Allrooms
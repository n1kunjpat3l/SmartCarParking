import pymysql
import pymysql.cursors
conn= pymysql.connect(host='localhost',user='rasp',password='pi',db='ITPCarPark',charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
a=conn.cursor()

carPark_ID="P6"
slotsAvailable=0
totalSlots=0

sqlGetTotal="select TotalCapacity from CarParks where CarParkID='%s'" %carPark_ID
a.execute(sqlGetTotal)
for row in a:
	totalSlots=row['TotalCapacity']
#print("Total Car Park Capacity: "+str(totalSlots))

sqlGetAvailableSlots="select SlotsAvailable from CarParkData where CarParkID='%s'" %carPark_ID
a.execute(sqlGetAvailableSlots)

for row in a:
	slotsAvailable=row['SlotsAvailable']
#print("Total Slots Available: "+str(slotsAvailable))

if slotsAvailable < totalSlots :
	#print("in if condition")
	sqlUpdate="update CarParkData set SlotsAvailable=SlotsAvailable + 1 where CarParkID='%s'" %carPark_ID
	try:
		a.execute(sqlUpdate)
		conn.commit()
		print("    Update Success !!")
	except:
		db.rollback()	

a.close()
conn.close()

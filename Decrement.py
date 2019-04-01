import pymysql
import pymysql.cursors
conn= pymysql.connect(host='localhost',user='rasp',password='pi',db='ITPCarPark',charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
a=conn.cursor()

carPark_ID="P6"
slotsAvailable=0

sqlGet="select SlotsAvailable from CarParkData where CarParkID='%s'" %carPark_ID
a.execute(sqlGet)

for row in a:
	slotsAvailable=row['SlotsAvailable']
#print("Total Slots Available: "+str(slotsAvailable))

if slotsAvailable > 0 :
	#print("in if condition")
	sqlUpdate="update CarParkData set SlotsAvailable=SlotsAvailable - 1 where CarParkID='%s'" %carPark_ID
	try:
		a.execute(sqlUpdate)
		conn.commit()
		print("    Update Success !!")
	except:
		conn.rollback()	

a.close()
conn.close()

import mysql.connector
import time
import requests
import json
import logging
import base64

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s.%(msecs)03d [%(levelname)s] %(message)s",
    datefmt="%m/%d/%Y %H:%M:%S",
)

if __name__ == "__main__":

        global data_old, data_new
        
        url = "https://jid.jasamargalive.com/client-api/add_object_r2"
 
        headers = {"Content-Type": "application/json",
                    "Authorization": "2345391662"}

        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="test"
        )

        cursor= mydb.cursor()
        cursor.execute("SELECT id FROM kr2")
        myresult = cursor.fetchall()
        
        f= open("data.txt","w+")
        f.write(str(myresult[len(myresult)-1][0]))
        f.close()

        i = 0

        while True:

            mydb1 = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="test"
            )

            try :
                cursor1= mydb1.cursor()
                cursor1.execute("SELECT id FROM kr2")
                myresult1 = cursor1.fetchall()
                data_new = str(myresult1[len(myresult1)-1][0])

                lines = tuple(open("data.txt", 'r'))
                data_old = lines[0]

                cursor2= mydb1.cursor()
                cursor2.execute("SELECT detect FROM kr2")
                myresult2 = cursor2.fetchall()
                data_gambar = str(myresult2[len(myresult2)-1][0])

                # with open(data_gambar, "rb") as img_file:
                #     b64_string = base64.b64encode(img_file.read())

                ulang = int(data_new) - int(data_old)

                for x in range(ulang, 0, -1):
                    if data_new != data_old:
                        data_add = {
                                "kode_lokasi":	"1",	
                                "jenis_r2" :	"Montor",
                                "gambar": "base64"
                            }
                        response = requests.post(url, headers=headers, json=data_add)
                        if (response.json()['status'] == 1):
                            
                            logging.info("status:" + str(response.json()['status']))
                            f= open("data.txt","w+")
                            f.write(str(myresult1[len(myresult1)-x][0]))
                            f.close()
                            print(myresult1[len(myresult1)-x][0])
                        elif (response.json()['status'] == 0):
                            logging.error("feedback error")
                        else:
                            logging.error("feedback error")

                    
                    
                print(f'hasil {myresult1[len(myresult1)-1][0]} hitung {i}')
                # print(data_new)
                # print(data_old)

                i+=1
                time.sleep(1)

            except mysql.connector.Error as err:
                logging.info(err.msg)
    

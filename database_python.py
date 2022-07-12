import mysql.connector
import asyncio
import requests
import json
import logging
import base64
import socket
import os

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s.%(msecs)03d [%(levelname)s] %(message)s",
    datefmt="%m/%d/%Y %H:%M:%S",
)

async def io_related():

    global data_old, data_new

    url = "https://jid.jasamargalive.com/client-api/add_object_r2"
    
    headers = {"Content-Type": "application/json",
                    "Authorization": "2345391662"}

    mydb = mysql.connector.connect( 
        host="localhost", #172.16.4.34
        user="root", #jmto_cctv
        password="", #jmt02021!#
        database="test" #nonvehicledb
    )
    
    cursor= mydb.cursor()
    cursor.execute("SELECT id FROM kr2") #id data
    myresult = cursor.fetchall()
        
    f= open("data.txt","w+")
    f.write(str(myresult[len(myresult)-1][0]))
    f.close()

    # i = 0

    while True:
        mydb1 = mysql.connector.connect(
                host="localhost", #172.16.4.34
                user="root", #jmto_cctv
                password="", #jmt02021!#
                database="test" #nonvehicledb
            )
            
        try :
            cursor1= mydb1.cursor()
            cursor1.execute("SELECT id FROM kr2") #id data
            myid = cursor1.fetchall()
            data_new = str(myid[len(myid)-1][0])

            lines = tuple(open("data.txt", 'r'))
            data_old = lines[0]

            cursor2= mydb1.cursor()
            cursor2.execute("SELECT id FROM kr2") #id_location data
            myid_location = cursor2.fetchall()
            id_location = str(myid_location[len(myid_location)-1][0])
            logging.info(f"id location:{id_location}")
            
            cursor3= mydb1.cursor()
            cursor3.execute("SELECT detect FROM kr2") #nonkr_details data
            mynonkr_gambar = cursor3.fetchall()
            nonkr_gambar = mynonkr_gambar[len(mynonkr_gambar)-1][0]
            logging.info(f"gambar:{nonkr_gambar[0:100]}")

            cursor4= mydb1.cursor()
            cursor4.execute("SELECT details FROM kr2") #nonkr_details data
            mynonkr_detail = cursor4.fetchall()
            nonkr_details = str(mynonkr_detail[len(mynonkr_detail)-1][0])
            logging.info(f"detail:{nonkr_details[0:100]}")
            
            # if os.stat(nonkr_details).st_size:
            #     with open(nonkr_details, "rb") as img_file:
            #         b64_string = base64.b64encode(img_file.read())
            #         logging.info("converted")

            # else:
            #     logging.error("no picture url")

            if len(nonkr_gambar) > 0:
                b64_string = base64.b64encode(nonkr_gambar)
                logging.info("converted")
                logging.info(b64_string[0:100])

                f= open("data_base64_.txt","w+")
                f.write(b64_string.decode())
                f.close()
            else:
                logging.error("no picture url")

            if data_new != data_old:
                data_add = {
                    "kode_lokasi": "1",	
                    "jenis_r2" : nonkr_details,
                    "gambar": b64_string.decode()                            
                }
                response = requests.post(url, headers=headers, json=data_add)
                        
                if (response.json()['status'] == 1):                          
                    logging.info("status:" + str(response.json()['status']))
                    logging.info("status_detail:" + str(response.json()))
                    f= open("data.txt","w+")
                    f.write(str(myid[len(myid)-1][0]))
                    f.close()
                    print(myid[len(myid)-1][0])
                elif (response.json()['status'] == 0):
                    logging.error("feedback error")
                else:
                    logging.error("feedback error")
                                    
            # print(f'hasil {myid[len(myid)-1][0]} hitung {i}')
                # print(data_new)
                # print(data_old)

            # i+=1

        except mysql.connector.Error as err:
            logging.error(err.msg)    

        await asyncio.sleep(0.5)

async def io_related2():
    while True:
        try:
            socket.gethostbyaddr('192.168.0.101')
            logging.info("device connected  ")

        except socket.herror:
            logging.info(u"device disconnected")
        await asyncio.sleep(1)
        

async def main():

    await asyncio.gather(
        io_related(),
        io_related2(),
    )  # 1s + 1s = over 1s

if __name__ == "__main__":

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
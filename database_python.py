import mysql.connector
import asyncio
import requests
import json
import logging
import base64
import socket
import os
import datetime
import configparser

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s.%(msecs)03d [%(levelname)s] %(message)s",
    datefmt="%m/%d/%Y %H:%M:%S",
)

config_obj2 = configparser.ConfigParser()
config_obj2.read("configfile.ini")
config_obj = config_obj2["configfile"]

url = "https://jid.jasamargalive.com/client-api/add_object_r2"

headers = {"Content-Type": "application/json",
                    "Authorization": "2345391662"}

async def io_related():

    global data_old, data_new
    url = "https://jid.jasamargalive.com/client-api/add_object_r2"
    mydb = mysql.connector.connect( 
        host=config_obj["host"],
        user=config_obj["user"],
        password=config_obj["password"], 
        database=config_obj["database"] 
    )
    
    cursor= mydb.cursor()
    cursor.execute("SELECT id FROM data ORDER BY id DESC LIMIT 2") #id data
    myresult = cursor.fetchall()
        
    f= open("data.txt","w+")
    f.write(str(myresult[0][0]))
    f.close()
    mydb.close()
    # i = 0

    while True:
        mydb1 = mysql.connector.connect(
                host=config_obj["host"], #172.16.4.34
                user=config_obj["user"], #jmto_cctv
                password=config_obj["password"], #jmt02021!#
                database=config_obj["database"] #nonvehicledb
            )
            
        try :
            cursor1= mydb1.cursor()
            cursor1.execute("SELECT id FROM data ORDER BY id DESC LIMIT 2") #id data
            myid = cursor1.fetchall()
            data_new = str(myid[0][0])
            logging.info(f"id :{data_new}")

            lines = tuple(open("data.txt", 'r'))
            data_old = lines[0]

            cursor1.execute("SELECT id_location FROM data ORDER BY id DESC LIMIT 2") #id_location data
            myid_location = cursor1.fetchall()
            id_location = str(myid_location[0][0])
            logging.info(f"id location:{id_location}")
            
            cursor1.execute("SELECT capture_highres FROM data ORDER BY id DESC LIMIT 2") #capture_highres data
            mynonkr_gambar = cursor1.fetchall()
            nonkr_gambar = mynonkr_gambar[0][0]
            logging.info(f"gambar:{nonkr_gambar[0:10]}")

            cursor1.execute("SELECT nonkr_details FROM data ORDER BY id DESC LIMIT 2") #nonkr_details data
            mynonkr_detail = cursor1.fetchall()
            nonkr_details = str(mynonkr_detail[0][0])
            logging.info(f"detail:{nonkr_details[0:10]}")
            
            # if os.stat(nonkr_details).st_size:
            #     with open(nonkr_details, "rb") as img_file:
            #         b64_string = base64.b64encode(img_file.read())
            #         logging.info("converted")

            # else:
            #     logging.error("no picture url")

            if len(nonkr_gambar) > 0:
                b64_string = base64.b64encode(nonkr_gambar)
                logging.info("converted")
                # logging.info(b64_string[0:100])

                # f= open("data_base64_.txt","w+")
                # f.write(b64_string.decode())
                # f.close()
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
                    logging.info("res status addobject:" + str(response.json()['status']))
                    # logging.info("status_detail:" + str(response.json()))
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
            mydb1.close()
        except mysql.connector.Error as err:
            logging.error(err.msg)    

        await asyncio.sleep(20)

async def io_related2():
    url2 = "https://jid.jasamargalive.com/client-api/object_r2/update_status_perangkat"    
    while True:
        try:
            socket.gethostbyaddr(config_obj["ipdevice"])
            logging.info("device connected")
            data_status_device = {
                        "kode_lokasi": "1",	
                        "status_perangkat" : "ON",
                        "waktu_update_status_perangkat": str(datetime.datetime.now())                           
                    }

        except socket.herror:
            
            logging.info(u"device disconnected")
            data_status_device = {
                        "kode_lokasi": "1",	
                        "status_perangkat" : "OFF",
                        "waktu_update_status_perangkat": str(datetime.datetime.now())                        
                    }

        response = requests.post(url2, headers=headers, json=data_status_device)
                    
        if (response.json()['status'] == 1):                          
            logging.info("res status device:" + str(response.json()['status']))
            # logging.info("status_detail:" + str(response.json()))

        elif (response.json()['status'] == 0):
            logging.error("feedback error")
        else:
            logging.error("feedback error")

        await asyncio.sleep(10)
        
async def io_related3():
    while True:
        url3 = "https://jid.jasamargalive.com/client-api/object_r2/update_status_koneksi" 
        try:
            socket.gethostbyaddr('8.8.8.8')
            logging.info("connection establish")
            data_status_connection = {
                        "kode_lokasi": "1",	
                        "status_koneksi" : "ON",
                        "waktu_update_koneksi": str(datetime.datetime.now())                            
                    }
        except socket.herror:
            logging.info(u"connection not establish")
            data_status_connection = {
                        "kode_lokasi": "1",	
                        "status_koneksi" : "OFF",
                        "waktu_update_koneksi": str(datetime.datetime.now())                                 
                    }
        response = requests.post(url3, headers=headers, json=data_status_connection)
                    
        if (response.json()['status'] == 1):                          
            logging.info("res status koneksi:" + str(response.json()['status']))
            # logging.info("status_detail:" + str(response.json()))
            
        elif (response.json()['status'] == 0):
            logging.error("feedback error")
        else:
            logging.error("feedback error")

        await asyncio.sleep(10)

async def main():

    await asyncio.gather(
        io_related(),
        io_related2(),
        io_related3(),
    )  # 1s + 1s = over 1s

if __name__ == "__main__":

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
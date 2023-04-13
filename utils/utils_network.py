import socket
import time
import threading

import re


###############################################################################



class Node_C:
    def __init__(self,pk,ip,port,record=None,on=False):
        self.pk=pk
        self.ip=ip
        self.port=port
        self.record=record
        self.on=on
        self.sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        
        self.th_recv=threading.Thread(target=self.recv_sock, args=(record,), daemon=True)

        self.msg=None


    def connect(self):
        n=1
        while True:
            try:
                self.sock.connect((self.ip,self.port))
                self.on=True
                self.th_recv.start()
                break
            except:
                if n > 5:
                    print(f"{self.pk} connecting error!")
                    break
                print(f"{n}차 재연결 시도 중")
                n+=1
                time.time(1)      


    def recv_sock(self,record):
        while self.on:
            try:
                data=self.sock.recv(2048).decode('ascii')
                i=data.find('Status:')
                #print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
                msg = data[i:i+150]
                #print(msg)

                pattern = r"Status:\s*(\S+)|StateOfCharge:\s*(\d+)|Location:\s*(-?\d+)\s*(-?\d+)\s*(-?\d+)|Temperature:\s*(\d+)"
                matches = re.findall(pattern, msg)
                status_dic = {}

                for match in matches:
                    if match[0]:
                        status_dic['Status'] = match[0]
                    elif match[1]:
                        status_dic['StateOfCharge'] = int(match[1])
                    elif match[2] and match[3] and match[4]:
                        status_dic['Location_x'] = float(match[2])
                        status_dic['Location_y'] = float(match[3])
                        status_dic['Location_z'] = float(match[4])
                    elif match[5]:
                        status_dic['Temperature'] = int(match[5])

                #print(status_dic)
                record.Status = status_dic["Status"]
                record.StateOfCharge = status_dic["StateOfCharge"]
                record.Location_x = status_dic["Location_x"]
                record.Location_y = status_dic["Location_y"]
                record.Location_z = status_dic["Location_z"]
                record.Temperature = status_dic["Temperature"]
                record.save()
                


            except:
                if self.on == True:
                    self.connect
                else:
                    break
            time.sleep(0.5)

        
    def send_sock(self,msg):
        if self.on == True:
            data=msg.encode()+b"\n"
            try:
                self.sock.send(data)
            except:
                print("fail_send")
        else:
            print("not connect!")


    def disconnect(self):
        self.sock.close()
        self.on=False




class NetworkController:
    def __init__(self):
        self.connected={}

        self.th_checkStatus=threading.Thread(target=self.checkStatus,daemon=True)
        self.th_checkStatus.start()

    def networkMaster(self):
        pass


    def checkStatus(self):
        while True:
            try:
                for nd in self.connected:
                    self.connected[nd].send_sock("onelinestatus")
                    time.sleep(0.1)
            except:
                pass

    
    def addConnect(self,pk,record):
        node = Node_C(pk,record.ip,record.port,record)

        try:
            node.connect()
            time.sleep(0.5)
            node.send_sock("admin")
            time.sleep(0.5)
            node.send_sock("say 연결에 성공했습니다!")
            self.connected[pk]=node
        except:
            print("addConnect_fail")

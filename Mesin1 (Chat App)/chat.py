import base64
import os
from os.path import join, dirname, realpath
import json
import uuid
import logging
from queue import  Queue
import threading 
import socket
import shutil
from datetime import datetime

class RealmThreadCommunication(threading.Thread):
    def __init__(self, chats, realm_dest_address, realm_dest_port):
        self.chats = chats
        self.chat = {}
        self.realm_dest_address = realm_dest_address
        self.realm_dest_port = realm_dest_port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.realm_dest_address, self.realm_dest_port))
        threading.Thread.__init__(self)

    def sendstring(self, string):
        try:
            self.sock.sendall(string.encode())
            receivedmsg = ""
            while True:
                data = self.sock.recv(1024)
                print("diterima dari server", data)
                if (data):
                    receivedmsg = "{}{}" . format(receivedmsg, data.decode())
                    if receivedmsg[-4:]=='\r\n\r\n':
                        print("end of string")
                        return json.loads(receivedmsg)
        except:
            self.sock.close()
            return { 'status' : 'ERROR', 'message' : 'Gagal'}
    
    def put(self, message):
        dest = message['msg_to']
        try:
            self.chat[dest].put(message)
        except KeyError:
            self.chat[dest]=Queue()
            self.chat[dest].put(message)

class Chat:
    def __init__(self):
        self.sessions={}
        self.users = {}
        self.group = {}
        self.users['messi']={ 'nama': 'Lionel Messi', 'negara': 'Argentina', 'password': 'surabaya', 'incoming' : {}, 'outgoing': {}}
        self.users['henderson']={ 'nama': 'Jordan Henderson', 'negara': 'Inggris', 'password': 'surabaya', 'incoming': {}, 'outgoing': {}}
        self.users['lineker']={ 'nama': 'Gary Lineker', 'negara': 'Inggris', 'password': 'surabaya','incoming': {}, 'outgoing':{}}
        self.realms = {}
    def proses(self,data):
        j=data.split(" ")
        try:
            command=j[0].strip()
            if (command=='auth'):
                username=j[1].strip()
                password=j[2].strip()
                logging.warning("AUTH: auth {} {}" . format(username,password))
                return self.autentikasi_user(username,password)
            
            elif (command=='register'):
                username=j[1].strip()
                password=j[2].strip()
                nama=j[3].strip()
                negara=j[4].strip()
                logging.warning("REGISTER: register {} {}" . format(username,password))
                return self.register_user(username,password, nama, negara)
            
#   ===================== Komunikasi dalam satu server =====================            
            elif (command=='addgroup'):
                sessionid = j[1].strip()
                groupname = j[2].strip()
                usernamefrom = self.sessions[sessionid]['username']
                logging.warning("ADDGROUP: session {} added group {}" . format(sessionid, groupname))
                return self.addgroup(sessionid,usernamefrom,groupname)
            elif (command == 'joingroup'):
                sessionid = j[1].strip()
                groupname = j[2].strip()
                usernamefrom = self.sessions[sessionid]['username']
                logging.warning("JOINGROUP: session {} added group {}" . format(sessionid, groupname))
                return self.joingroup(sessionid, usernamefrom, groupname)
            elif (command=='send'):
                sessionid = j[1].strip()
                usernameto = j[2].strip()
                message=""
                for w in j[3:]:
                    message="{} {}" . format(message,w)
                usernamefrom = self.sessions[sessionid]['username']
                logging.warning("SEND: session {} send message from {} to {}" . format(sessionid, usernamefrom,usernameto))
                return self.send_message(sessionid,usernamefrom,usernameto,message)
            elif (command=='sendgroup'):
                sessionid = j[1].strip()
                groupname = j[2].strip()
                message=""
                for w in j[3:]:
                    message="{} {}" . format(message,w)
                usernamefrom = self.sessions[sessionid]['username']
                logging.warning("SEND: session {} send message from {} to {}" . format(sessionid, groupname, usernamefrom,groupname))
                return self.send_group_message(sessionid,groupname, usernamefrom,message)
            elif (command=='inbox'):
                sessionid = j[1].strip()
                username = self.sessions[sessionid]['username']
                logging.warning("INBOX: {}" . format(sessionid))
                return self.get_inbox(username)
            elif (command=='sendfile'):
                sessionid = j[1].strip()
                usernameto = j[2].strip()
                filepath = j[3].strip()
                encoded_file = j[4].strip()
                usernamefrom = self.sessions[sessionid]['username']
                logging.warning("SENDFILE: session {} send file from {} to {}" . format(sessionid, usernamefrom, usernameto))
                return self.send_file(sessionid, usernamefrom, usernameto, filepath, encoded_file)
            elif (command=='sendgroupfile'):
                sessionid = j[1].strip()
                groupname = j[2].strip()
                filepath = j[3].strip()
                encoded_file = j[4].strip()
                usernamefrom = self.sessions[sessionid]['username']
                logging.warning("SENDGROUPFILE: session {} send file from {} to {}" . format(sessionid, usernamefrom, groupname))
                return self.send_group_file(sessionid, usernamefrom, groupname, filepath, encoded_file)
            
            #   ===================== Komunikasi dalam satu server =====================            
            elif command == "addrealm":
                realm_id = j[1].strip()
                realm_dest_address = j[2].strip()
                realm_dest_port = int(j[3].strip())
                return self.add_realm(
                    realm_id, realm_dest_address, realm_dest_port, data
            )

            elif command == "recvrealm":
                realm_id = j[1].strip()
                realm_dest_address = j[2].strip()
                realm_dest_port = int(j[3].strip())
                return self.recv_realm(
                    realm_id, realm_dest_address, realm_dest_port, data
            )

            elif command == "sendgrouprealm":
                sessionid = j[1].strip()
                realm_id = j[2].strip()
                usernamesto = j[3].strip()
                message = ""
                for w in j[4:]:
                    message = "{} {}".format(message, w)
                usernamefrom = self.sessions[sessionid]["username"]
                logging.warning(
                    "SENDGROUPREALM: session {} send message from {} to {} in realm {}".format(
                        sessionid, usernamefrom, usernamesto, realm_id
                    )
                )
                return self.send_group_realm_message(
                    sessionid, realm_id, usernamefrom, usernamesto, message, data
                )
                
            elif command == 'getgrouprealm':
                groupname = j[2].strip()
                logging.warning("GETGROUPREALM: groupname {}" . format(groupname))
                return self.get_group_members(groupname)

            elif command == "recvrealmgroupmsg":
                usernamefrom = j[1].strip()
                realm_id = j[2].strip()
                usernamesto = j[3].strip().split(",")
                message = ""
                for w in j[4:]:
                    message = "{} {}".format(message, w)
                logging.warning(
                    "RECVGROUPREALM: send message from {} to {} in realm {}".format(
                        usernamefrom, usernamesto, realm_id
                    )
                )
                return self.recv_group_realm_message(
                    realm_id, usernamefrom, usernamesto, message, data
                )
            
            elif command == "sendgroupfilerealm":
                sessionid = j[1].strip()
                realm_id = j[2].strip()
                usernamesto = j[3].strip()
                filepath = j[4].strip()
                encoded_file = j[5].strip()
                usernamefrom = self.sessions[sessionid]["username"]
                logging.warning(
                    "SENDGROUPFILEREALM: session {} send file from {} to {} in realm {}".format(
                        sessionid, usernamefrom, usernamesto, realm_id
                    )
                )
                return self.send_group_file_realm(
                    sessionid,
                    realm_id,
                    usernamefrom,
                    usernamesto,
                    filepath,
                    encoded_file,
                    data,
                )

            elif command == "recvgroupfilerealm":
                realm_id = j[2].strip()
                groupname_or_usernames = j[3].strip()
                filepath = j[4].strip()
                encoded_file = j[5].strip()
                usernamefrom = j[1].strip()
                logging.warning(
                    "RECVGROUPFILEREALM: receive file from {} to group {} in realm {}".format(
                        usernamefrom, groupname_or_usernames, realm_id
                    )
                )
                return self.recv_group_file_realm(
                    realm_id, usernamefrom, groupname_or_usernames, filepath, encoded_file, data
                )

            elif (command=='logout'):
                sessionid = j[1].strip()
                return  self.logout(sessionid)
            elif (command=='info'):
                return self.info()
            else:
                print(command)
                return {'status': 'ERROR', 'message': '**Protocol Tidak Benar'}
        except KeyError:
            return { 'status': 'ERROR', 'message' : 'Informasi tidak ditemukan'}
        except IndexError:
            return {'status': 'ERROR', 'message': '--Protocol Tidak Benar'}

    def autentikasi_user(self,username,password):
        if (username not in self.users):
            return { 'status': 'ERROR', 'message': 'User Tidak Ada' }
        if (self.users[username]['password']!= password):
            return { 'status': 'ERROR', 'message': 'Password Salah' }
        tokenid = str(uuid.uuid4()) 
        self.sessions[tokenid]={ 'username': username, 'userdetail':self.users[username]}
        return { 'status': 'OK', 'tokenid': tokenid }
    
    def register_user(self,username, password, nama, negara):
        if (username in self.users):
            return { 'status': 'ERROR', 'message': 'User Sudah Ada' }
        nama = nama.replace("_", " ")
        self.users[username]={ 
            'nama': nama,
            'negara': negara,
            'password': password,
            'incoming': {},
            'outgoing': {}
            }
        tokenid = str(uuid.uuid4()) 
        self.sessions[tokenid]={ 'username': username, 'userdetail':self.users[username]}
        return { 'status': 'OK', 'tokenid': tokenid }

    def get_user(self,username):
        if (username not in self.users):
            return False
        return self.users[username]
    
    def get_group(self, group_name):
        if (group_name not in self.group):
            return False
        return self.group[group_name]

#   ===================== Komunikasi dalam satu server =====================
    def addgroup(self, sessionid, usernamefrom, groupname):
        if (sessionid not in self.sessions):
            return {'status': 'ERROR', 'message': 'Session Tidak Ditemukan'}
        self.group[groupname]={
            'admin': usernamefrom,
            'members': [usernamefrom],
            'message':{}
        }
        return {'status': 'OK', 'message': 'Add group successful'}
    
    def joingroup(self, sessionid, usernamefrom, groupname):
        if (sessionid not in self.sessions):
            return {'status': 'ERROR', 'message': 'Session Tidak Ditemukan'}
        if usernamefrom in self.group[groupname]['members']:
            return {'status': 'ERROR', 'message': 'User sudah dalam group'}
        self.group[groupname]['members'].append(usernamefrom)
        return {'status': 'OK', 'message': 'Join group successful'}
    
    def send_message(self,sessionid,username_from,username_dest,message):
        if (sessionid not in self.sessions):
            return {'status': 'ERROR', 'message': 'Session Tidak Ditemukan'}
        s_fr = self.get_user(username_from)
        s_to = self.get_user(username_dest)

        if (s_fr==False or s_to==False):
            return {'status': 'ERROR', 'message': 'User Tidak Ditemukan'}

        message = { 'msg_from': s_fr['nama'], 'msg_to': s_to['nama'], 'msg': message }
        outqueue_sender = s_fr['outgoing']
        inqueue_receiver = s_to['incoming']
        try:	
            outqueue_sender[username_from].put(message)
        except KeyError:
            outqueue_sender[username_from]=Queue()
            outqueue_sender[username_from].put(message)
        try:
            inqueue_receiver[username_from].put(message)
        except KeyError:
            inqueue_receiver[username_from]=Queue()
            inqueue_receiver[username_from].put(message)
        return {'status': 'OK', 'message': 'Message Sent'}
    
    def send_group_message(self, sessionid, groupname, username_from, message):
        if (sessionid not in self.sessions):
            return {'status': 'ERROR', 'message': 'Session Tidak Ditemukan'}
        s_fr = self.get_user(username_from)
        if s_fr is False:
            return {'status': 'ERROR', 'message': 'User Tidak Ditemukan'}
        for username_dest in self.group[groupname]['members']:
            s_to = self.get_user(username_dest)
            if s_to is False:
                continue
            message = {'group': groupname,'msg_from': s_fr['nama'], 'msg_to': s_to['nama'], 'msg': message}
            try:    
                self.group[groupname]['message'][username_from].put(message)
            except KeyError:
                self.group[groupname]['message'][username_from]=Queue()
                self.group[groupname]['message'][username_from].put(message)
            
            outqueue_sender = s_fr['outgoing']
            inqueue_receiver = s_to['incoming']
            try:    
                outqueue_sender[username_from].put(message)
            except KeyError:
                outqueue_sender[username_from]=Queue()
                outqueue_sender[username_from].put(message)
            try:
                inqueue_receiver[username_from].put(message)
            except KeyError:
                inqueue_receiver[username_from]=Queue()
                inqueue_receiver[username_from].put(message)
        return {'status': 'OK', 'message': 'Message Sent'}
    
    def get_inbox(self,username):
        s_fr = self.get_user(username)
        incoming = s_fr['incoming']
        msgs={}
        for users in incoming:
            msgs[users]=[]
            while not incoming[users].empty():
                msgs[users].append(s_fr['incoming'][users].get_nowait())
        return {'status': 'OK', 'messages': msgs}

    def send_file(self, sessionid, username_from, username_dest, filepath ,encoded_file):
        if sessionid not in self.sessions:
            return {'status': 'ERROR', 'message': 'Session Tidak Ditemukan'}
        
        s_fr = self.get_user(username_from)
        s_to = self.get_user(username_dest)

        if s_fr is False or s_to is False:
            return {'status': 'ERROR', 'message': 'User Tidak Ditemukan'}

        filename = os.path.basename(filepath)
        message = {
            'msg_from': s_fr['nama'],
            'msg_to': s_to['nama'],
            'file_name': filename,
            'file_content': encoded_file
        }

        outqueue_sender = s_fr['outgoing']
        inqueue_receiver = s_to['incoming']
        try:
            outqueue_sender[username_from].put(json.dumps(message))
        except KeyError:
            outqueue_sender[username_from] = Queue()
            outqueue_sender[username_from].put(json.dumps(message))
        try:
            inqueue_receiver[username_from].put(json.dumps(message))
        except KeyError:
            inqueue_receiver[username_from] = Queue()
            inqueue_receiver[username_from].put(json.dumps(message))
        
        # Simpan file ke folder dengan nama yang mencerminkan waktu pengiriman dan nama asli file
        now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        folder_name = f"{now}_{username_from}_{username_dest}_{filename}"
        folder_path = join(dirname(realpath(__file__)), 'files/')
        os.makedirs(folder_path, exist_ok=True)
        folder_path = join(folder_path, folder_name)
        os.makedirs(folder_path, exist_ok=True)
        file_destination = os.path.join(folder_path, filename)
        if 'b' in encoded_file[0]:
            msg = encoded_file[2:-1]

            with open(file_destination, "wb") as fh:
                fh.write(base64.b64decode(msg))
        else:
            tail = encoded_file.split()
        
        return {'status': 'OK', 'message': 'File Sent'}

    def send_group_file(self, sessionid, username_from, groupname, filepath, encoded_file):
        if (sessionid not in self.sessions):
            return {'status': 'ERROR', 'message': 'Session Tidak Ditemukan'}
        s_fr = self.get_user(username_from)
        if s_fr is False:
            return {'status': 'ERROR', 'message': 'User Tidak Ditemukan'}

        filename = os.path.basename(filepath)
        for username_dest in self.group[groupname]['members']:
            s_to = self.get_user(username_dest)
            if s_to is False:
                continue
            message = {
                'group': groupname,
                'msg_from': s_fr['nama'],
                'msg_to': s_to['nama'],
                'file_name': filename,
                'file_content': encoded_file
            }

            try:    
                self.group[groupname]['message'][username_from].put(message)
            except KeyError:
                self.group[groupname]['message'][username_from]=Queue()
                self.group[groupname]['message'][username_from].put(message)
            
            outqueue_sender = s_fr['outgoing']
            inqueue_receiver = s_to['incoming']
            try:
                outqueue_sender[username_from].put(json.dumps(message))
            except KeyError:
                outqueue_sender[username_from] = Queue()
                outqueue_sender[username_from].put(json.dumps(message))
            try:
                inqueue_receiver[username_from].put(json.dumps(message))
            except KeyError:
                inqueue_receiver[username_from] = Queue()
                inqueue_receiver[username_from].put(json.dumps(message))
        
            # Simpan file ke folder dengan nama yang mencerminkan waktu pengiriman dan nama asli file
            now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            folder_name = f"{now}_{username_from}_{username_dest}_{filename}"
            folder_path = join(dirname(realpath(__file__)), 'files/')
            os.makedirs(folder_path, exist_ok=True)
            folder_path = join(folder_path, folder_name)
            os.makedirs(folder_path, exist_ok=True)
            file_destination = os.path.join(folder_path, filename)
            if 'b' in encoded_file[0]:
                msg = encoded_file[2:-1]

                with open(file_destination, "wb") as fh:
                    fh.write(base64.b64decode(msg))
            else:
                tail = encoded_file.split()
        
        return {'status': 'OK', 'message': 'File Sent'}
    
     #   ===================== Komunikasi dengan server lain =====================
    def add_realm(self, realm_id, realm_dest_address, realm_dest_port, data):
        j = data.split()
        j[0] = "recvrealm"
        data = " ".join(j)
        data += "\r\n"
        if realm_id in self.realms:
            return {"status": "ERROR", "message": "Realm sudah ada"}

        self.realms[realm_id] = RealmThreadCommunication(
            self, realm_dest_address, realm_dest_port
        )
        result = self.realms[realm_id].sendstring(data)
        return result
    
    def recv_realm(self, realm_id, realm_dest_address, realm_dest_port, data):
        self.realms[realm_id] = RealmThreadCommunication(
            self, realm_dest_address, realm_dest_port
        )
        return {"status": "OK"}
    
    def get_group_members(self, groupname):
        group = self.get_group(groupname)
        if not group:
            return {"status": "ERROR", "message": "Group Tidak Ditemukan"}
        members = group['members']
        return {"status": "OK", "members": members}

    def send_group_realm_message(
        self, sessionid, realm_id, username_from, groupname_or_usernames, message, data
    ):
        if sessionid not in self.sessions:
            return {"status": "ERROR", "message": "Session Tidak Ditemukan"}
        if realm_id not in self.realms:
            return {"status": "ERROR", "message": "Realm Tidak Ditemukan"}
        s_fr = self.get_user(username_from)

        # Check if the groupname_or_usernames is a group or usernames
        if groupname_or_usernames.startswith("group:"):
            groupname = groupname_or_usernames.split("group:")[1]
            # Request to get group members from the target realm
            j = data.split()
            j[0] = "getgrouprealm"
            j[2] = groupname
            data = " ".join(j)
            data += "\r\n"
            members_response = self.realms[realm_id].sendstring(data)
            if members_response["status"] != "OK":
                return {"status": "ERROR", "message": "Group Tidak Ditemukan di Realm"}
            usernames_to = members_response["members"]
        else:
            usernames_to = groupname_or_usernames.split(",")
        
        for username_to in usernames_to:
            s_to = self.get_user(username_to)
            message_data = {"msg_from": s_fr["nama"], "msg_to": s_to["nama"], "msg": message.strip()}
            print(message_data)
            self.realms[realm_id].put(message_data)
        # print("data", data)
        # logging.warning(data)
        j = data.split()
        j[0] = "recvrealmgroupmsg"
        j[1] = username_from
        j[2] = realm_id
        j[3] = ",".join(usernames_to)
        data = " ".join(j)
        data += "\r\n"
        logging.warning(data)
        self.realms[realm_id].sendstring(data)
        return {"status": "OK", "message": "Message Sent to Group in Realm"}
    

    def recv_group_realm_message(
        self, realm_id, username_from, usernames_to, message, data
    ):
        logging.warning("recv_group_realm_message called with data: {}".format(data))
        if realm_id not in self.realms:
            return {"status": "ERROR", "message": "Realm Tidak Ditemukan"}
        s_fr = self.get_user(username_from)
        if not s_fr:
            return {"status": "ERROR", "message": "User Tidak Ditemukan"}
        for username_to in usernames_to:
            s_to = self.get_user(username_to)
            if not s_to:
                logging.warning("User {} not found".format(username_to))
                continue
            message_data = {"msg_from": s_fr["nama"], "msg_to": s_to["nama"], "msg": message.strip()}
            
            inqueue_receiver = s_to['incoming']
            if username_from not in inqueue_receiver:
                inqueue_receiver[username_from] = Queue()
            inqueue_receiver[username_from].put(message_data)
        
        logging.warning("Message stored successfully: {}".format(message_data))
        return {"status": "OK", "message": "Message Sent to Group in Realm"}

    def send_group_file_realm(
        self,
        sessionid,
        realm_id,
        username_from,
        groupname_or_usernames,
        filepath,
        encoded_file,
        data,
    ):
        if sessionid not in self.sessions:
            return {"status": "ERROR", "message": "Session Tidak Ditemukan"}
        if realm_id not in self.realms:
            return {"status": "ERROR", "message": "Realm Tidak Ditemukan"}
        s_fr = self.get_user(username_from)

        if s_fr == False:
            return {"status": "ERROR", "message": "User Tidak Ditemukan"}
        
        usernames_to = []
        if groupname_or_usernames.startswith("group:"):
            groupname = groupname_or_usernames.split("group:")[1]
            # Request to get group members from the target realm
            j = data.split()
            j[0] = "getgrouprealm"
            j[2] = groupname
            data = " ".join(j)
            data += "\r\n"
            members_response = self.realms[realm_id].sendstring(data)
            if members_response["status"] != "OK":
                return {"status": "ERROR", "message": "Group Tidak Ditemukan di Realm"}
            usernames_to = members_response["members"]
        else:
            usernames_to = groupname_or_usernames.split(",")

        filename = os.path.basename(filepath)
        for username_to in usernames_to:
            s_to = self.get_user(username_to)
            message = {
                "msg_from": s_fr["nama"],
                "msg_to": s_to["nama"],
                "file_name": filename,
                "file_content": encoded_file,
            }
            self.realms[realm_id].put(message)

            now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            folder_name = f"{now}_{username_from}_{username_to}_{filename}"
            folder_path = join(dirname(realpath(__file__)), "../Mesin2 (Chat App)/files/")
            os.makedirs(folder_path, exist_ok=True)
            folder_path = join(folder_path, folder_name)
            os.makedirs(folder_path, exist_ok=True)
            file_destination = os.path.join(folder_path, filename)
            if "b" in encoded_file[0]:
                msg = encoded_file[2:-1]

                with open(file_destination, "wb") as fh:
                    fh.write(base64.b64decode(msg))
            else:
                tail = encoded_file.split()

        j = data.split()
        logging.warning(j)
        j[0] = "recvrealmgroupmsg"
        j[1] = username_from
        j[2] = realm_id
        j[3] = ",".join(usernames_to)
        data = " ".join(j)
        data += "\r\n"
        self.realms[realm_id].sendstring(data)
        return {"status": "OK", "message": "Message Sent to Group in Realm"}

    def recv_group_file_realm(
        self, realm_id, username_from, groupname_or_usernames, filepath, encoded_file, data
    ):
        if realm_id not in self.realms:
            return {"status": "ERROR", "message": "Realm Tidak Ditemukan"}
        s_fr = self.get_user(username_from)

        if s_fr == False:
            return {"status": "ERROR", "message": "User Tidak Ditemukan"}

        filename = os.path.basename(filepath)
        if groupname_or_usernames.startswith("group:"):
            groupname = groupname_or_usernames.split("group:")[1]
            group = self.get_group(groupname)
            if not group:
                return {"status": "ERROR", "message": "Group Tidak Ditemukan"}
            usernames_to = group['members']
        else:
            usernames_to = groupname_or_usernames.split(",")

        for username_to in usernames_to:
            s_to = self.get_user(username_to)
            message = {
                "msg_from": s_fr["nama"],
                "msg_to": s_to["nama"],
                "file_name": filename,
                "file_content": encoded_file,
            }

            # Store the message in the incoming queue of the recipient
            inqueue_receiver = s_to['incoming']
            if username_from not in inqueue_receiver:
                inqueue_receiver[username_from] = Queue()
            inqueue_receiver[username_from].put(message)

            # Save the file locally
            now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            folder_name = f"{now}_{username_from}_{username_to}_{filename}"
            folder_path = join(dirname(realpath(__file__)), "files/")
            os.makedirs(folder_path, exist_ok=True)
            folder_path = join(folder_path, folder_name)
            os.makedirs(folder_path, exist_ok=True)
            file_destination = os.path.join(folder_path, filename)
            if "b" in encoded_file[0]:
                msg = encoded_file[2:-1]

                with open(file_destination, "wb") as fh:
                    fh.write(base64.b64decode(msg))
            else:
                tail = encoded_file.split()

        return {"status": "OK", "message": "File Received from Group in Realm"}

    
    def logout(self, sessionid):
        if (bool(self.sessions) == True):
            del self.sessions[sessionid]
            return {'status': 'OK'}
        else:
            return {'status': 'ERROR', 'message': 'Belum Login'}
    def info(self):
        return {'status': 'OK', 'message': self.sessions}

if __name__=="__main__":
    j = Chat()
    sesi = j.proses("auth messi surabaya")
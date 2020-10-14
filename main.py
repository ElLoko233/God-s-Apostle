try:
	import subprocess, os, re, datetime, sys, shutil
	from send2trash import send2trash
except ModuleNotFoundError:
	print(f"You don't have the required module installed to run the program\nYou need [subprocess, re, sys, os, send2trash] installed")

 
if __name__ == "__main__":
	# accessing the command from command line
	command = sys.argv[-1]

	if command == "RemoveHistory":
		# Access the logs and delete all files
		log_pattern = re.compile(".*(_log[s]?)", re.IGNORECASE)

		# Iterating through folders and directories in current working directory
		for file in os.listdir():

			# Testing if 'file' meets the criteria and that it is a directory
			if re.match(log_pattern, file) and os.path.isdir(file):

				# Sending match to trash///future delete folders completely
				send2trash(file)

	elif command == "TurnOff":
		# Kill a running a process 
		kill_running(name="python")

	elif command == "SelfDistruct":
		# Kill a running a process 
		kill_running(name="python")

		# Removing folder contents
		countdown = len(os.listdir())
		for file in os.listdir('./'):
			print(countdown)
			send2trash(file)
			countdown -= 1
		else:
			print("Boom!!!")

	elif command == "AutoSendLogs":
		# Running script in background
		subprocess.Popen("python bg_run.py", stdout=subprocess.DEVNULL,
						startupinfo=process, creationflags=subprocess.CREATE_NO_WINDOW,
						 start_new_session=True,
						)
		
	elif command in os.listdir() and command != "main.py":
		pass

	else: 
		#Print error code
		#Print opt
		print("No Match")

class Apostle:
	"""
	Manages the running loggers and ensures that only one logger is running.
	"""

	# Subprocess startupinfo
	process = subprocess.STARTUPINFO(dwFlags=subprocess.STARTF_USESHOWWINDOW)

	@classmethod
	def kill_running(cls):
		"""
		task: Takes care of killing processes
		"""

		# Access the PIDs from a file
		try:
			with open("./__cache__/__t_init__.tix", 'r') as file:
				# List of saved PIDs
				pyPID = [PID for PID in file.readlines()]
		
		except (FileNotFoundError, FileExistsError):
			os.makedir("./__cache__/")
			pyPID = []

		# killing the processes
		for PID in pyPID:
			# Killing process by PID and any child processes started by it
			task = subprocess.Popen(f"taskkill /f /pid {PID} /t", shell=True, stdout=subprocess.PIPE,
							startupinfo=cls.process, creationflags=subprocess.CREATE_NO_WINDOW,
							 start_new_session=True, stderr=subprocess.PIPE, text=True)
		else:
			return task


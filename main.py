try:
	import subprocess, os, re, datetime, sys
	from send2trash import send2trash
except ModuleNotFoundError:
	print(f"You dont have the required module installed to run the program\nYou need [subprocess, re, sys, os] installed")
"""
This file manages the running loggers and ensures that only one logger is running.
"""

def get_PID(tmd="00:00:00", name=" "):
	"""
	tmd: The time delta of the logger initialization
	return: a list of all PID's of a process than ran for a certain amount of time
	"""
	# Filter tmd to time format
	dt_pattern = re.compile(".*(?P<hour>\d{1,2}):(?P<minute>\d{1,2}):(?P<second>\d{1,2}).*", re.IGNORECASE) 
	match = re.match(dt_pattern, str(tmd))

	match = match.groupdict()
	tmd = f"{match.get('hour')}:{match.get('minute')}:{match.get('second')}"

	# Aquiring list of all processes that ran for that tmd
	Tasks = subprocess.Popen(f'tasklist /fi "CPUTIME ge {tmd}" ', 
		shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, start_new_session=subprocess.CREATE_NO_WINDOW)

	# Pattern to detect the name and PID of the application
	pattern = re.compile(f'^(?P<application>{name}.exe)[\s]*(?P<PID>[\d.]+)', re.IGNORECASE)

	pyTasks = []
	for task in list(Tasks.stdout):
		# Testing each line for a python process
		match = re.match(pattern, task)
		if match:
			# adding the PID of a python process to the list
			pyTasks.append(match.groupdict().get('PID'))
	else:
		return pyTasks

def get_tmdelta():
	# Gets the time delta between to points in time

	# Aquiring the time init
	try:
		with open('./__cache__/__t_init__.tix', 'r') as file:
			# matching the date time info from saved in the file
			dt_pattern = re.compile(".*(?P<year>[\d]{4})-(?P<month>[\d]{1,2})-(?P<date>[\d]{1,2}).*(?P<hour>[\d]{1,2}):(?P<minute>[\d]{1,2}):(?P<second>[\d]{1,2}).*", re.IGNORECASE)
			
			match = re.search(dt_pattern, file.read())
			match = match.groupdict()

			time_init = datetime.datetime(int(match.get('year')), int(match.get('month')), int(match.get('date')), int(match.get('hour')), int(match.get('minute')), int(match.get('second')))
	except (FileExistsError, FileNotFoundError, AttributeError, TypeError) as e:
		time_init = datetime.datetime.now()

	finally:
		timedelta = datetime.datetime.now().replace(microsecond=0) - time_init.replace(microsecond=0)
		return timedelta

def kill_running(name=" "):
	"""
	: Takes care of killing processes that are running
	"""

	# Aquiring the time delta of running process
	timedelta = get_tmdelta()

	# Aquiring PID of processes
	pyTasks = get_PID(tmd=timedelta, name=name)

	# killing the processes
	for task in pyTasks:
		# Killing process by Pid and any child processes started by it
		task = subprocess.Popen(f"taskkill /f /pid {task} /t", shell=True, start_new_session=subprocess.CREATE_NO_WINDOW, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
	else:
		return 1

 
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

				# Sending match to trash///future delete folders compelely
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
		#Run script that will send logs
		#End main.py
		print("Logs will send")

	elif command in os.listdir() and command != "main.py":
		# Test if match is a py file
		# run the match in background
		# record init time in file
		#End main.py
		print(command)

	else: 
		#Print error code
		#Print opt
		print("No Match")
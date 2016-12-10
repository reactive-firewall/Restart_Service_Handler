#! /usr/bin/env python

#
# Event handler script for restarting a nagios service on the local machine
# Idea taken from the Nagios documentation and re-designed and implemented in python
# see https://assets.nagios.com/downloads/nagioscore/docs/nagioscore/4/en/eventhandlers.html
# adapted by Kendrick Walls
#
# Copyright (c) 2016, Kendrick Walls
#	
#	Licensed under the Apache License, Version 2.0 (the "License");
#		you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#	   
#	   http://www.apache.org/licenses/LICENSE-2.0
#   
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import argparse

def parseArgs():
	"""Parse the Arguments."""
	parser = argparse.ArgumentParser(prog="restart_service.py", description='Handles service restart', epilog="Event handler script for restarting a nagios service on the target machine")
	parser.add_argument('status', choices=['OK','WARNING','PENDING','UNKNOWN','CRITICAL'], help='the service status')
	parser.add_argument('state', choices=['SOFT', 'HARD'], help='the service state')
	parser.add_argument('check_count', type=int, help='the service state count')
	parser.add_argument('host_name', help='the host running the service')
	parser.add_argument('service_cmd', help='the service restart script')
	parser.add_argument('service_name', help='the service to restart')
	parser.add_argument('-E', '--threshold', dest='threshold', default=3, required=False, help='the threshold at which to take action')
	group_action = parser.add_mutually_exclusive_group()
	group_action.add_argument('-C', '--crit-happens', default=True, action='store_true', dest='crit_happens', help='crit happens - allow hard critical state before taking action, overrides other preferences')
	group_action.add_argument('-D', '--crit-is-down', action='store_false', dest='crit_happens', help='crit avoidence - never wait for critical state before taking action, overrides other preferences')
	remote_action = parser.add_mutually_exclusive_group()
	remote_action.add_argument('--use-nrpe', default=True, action='store_true', dest='use_nrpe', help='use NRPE plugin - for remote hosts comunicate over NRPE, overrides other preferences. This is default.')
	remote_action.add_argument('--use-ssh', action='store_false', dest='use_nrpe', help='use SSH - for remote hosts communicate over SSH, overrides other preferences')
	remote_action.add_argument('--use-local', action='store_true', dest='use_local', default=False, help='use local - for remote hosts communicate to this command, overrides other preferences. Useful for hardcoding.')
	ssh_action = remote_action.add_argument_group()
	ssh_action.add_argument('--ssh-user', dest='ssh_user', default='nagios', help='SSH USER- for remote hosts communicate over SSH')
	ssh_action.add_argument('--ssh-password', dest='ssh_password', default='nagios', help='SSH PASSWORD- for remote hosts communicate over SSH. UNSAFE IN PROD.')
	ssh_action.add_argument('--ssh-key', dest='ssh_id', default='~/.id_rsa_4692', help='SSH Idenity Key- for remote hosts communicate over SSH')
	parser.add_argument('-V', '--version', action='version', version='%(prog)s 0.9.10')
	return parser.parse_args()


# define the function blocks
def ok_handler(state_mode="SOFT", count_num=1, action_threshold=3, crit_happens=True):
	"""Handler for when OK. Usualy nothing to do when it is all OK."""
	return False

def warn_handler(state_mode="SOFT", count_num=1, action_threshold=3, crit_happens=True):
	"""Handler for Warning state."""
	if state_options[state_mode]:
		if count_num >= action_threshold:
			return (crit_happens is False)
		else:
			return False
	else:
		return False

def crit_handler(state_mode="SOFT", count_num=1, action_threshold=3, crit_happens=True):
	"""Handler for Critical state."""
	if state_options[state_mode]:
		if count_num == action_threshold:
			return True
		else:
			# no need to be obsesive, call for user on HARD Fail
			return False
	else:
		return (crit_happens is False)

def unknown_handler(state_mode="SOFT", count_num=1, action_threshold=3, crit_happens=True):
	"""Handler for Warning state."""
	return True

def pending_handler(state_mode="SOFT", count_num=1, action_threshold=3, crit_happens=True):
	"""Handler for Pending state."""
	if state_options[state_mode]:
		if count_num >= action_threshold:
			return (crit_happens is False)
	return False

def getTimeStamp():
	"""Returns the time stamp."""
	theDate=None
	try:
		import time
		theDate = time.strftime("%a %b %d %H:%M:%S %Z %Y", time.localtime())
	except Exception:
		theDate=str("")
	return str(theDate)

def doErrorHandle(theInputStr):
	"""Handler for Error state."""
	try:
		import os
		import subprocess
		try:
			theResult=subprocess.check_output(str(theInputStr).split(' '))
		except Exception:
			timestamp = getTimeStamp()
			theResult = str(timestamp+" - WARNING - An error occured while handling the failure. Cascading failure.")
	except Exception:
		theResult = str("CRITICAL - An error occured while handling the cascading failure.")
		return theResult

# map the inputs to the function blocks
status_options = {"OK" : ok_handler,
	"WARNING" : warn_handler,
	"UNKNOWN" : unknown_handler,
	"PENDING" : pending_handler,
	"CRITICAL" : crit_handler
}

# map the states to the conditional blocks if state then
state_options = {"SOFT" : False,
	"HARD" : True,
	"UNKNOWN" : False
}

# could do something per count too
#count_options = {1 : first_handler,
#	2 : second_handler,
#	3 : last_handler,
#	4 : error_handler
#}

def main():
	args = parseArgs()
	status = str(args.status).upper()
	state = str(args.state).upper()
	action_threshold=None
	try:
		count = int(str(args.check_count), 10)
	except Exception as cerr:
		print(str(cerr))
		print(str(cerr.args))
		print(str(" UNKNOWN - An error occured while handling the arguments. Command failure."))
		exit(3)
	host_name = (args.host_name)
	service_cmd = (args.service_cmd)
	service_name = (args.service_name)
	use_nrpe = (args.use_nrpe)
	use_local = (args.use_local)

	crit_happens = (args.crit_happens is True)
	try:
		action_threshold=int(str(args.threshold), 10)
	except Exception as cerr:
		action_threshold=4
	if action_threshold is None:
		action_threshold = 4
	try:
		if status_options[status](state, count, action_threshold, crit_happens):
		# fix it
			timestamp = getTimeStamp()
			print(str(timestamp+" - Restarting service "+str(service_name)+" (" + str(state) + " critical state "+str(count)+"/"+str(action_threshold)+")...\n"))
			if ("localhost" not in str(host_name).lower()) and (use_local is False):
				if (use_nrpe is True):
					# Call NRPE to restart the service on the remote machine
					print( doErrorHandle("/usr/lib/nagios/plugins/check_nrpe -H "+str(host)+" -c "+str(service_cmd) ) )
				else:
					# Call SSH to restart the service on the remote machine
					print( doErrorHandle("/usr/bin/ssh -2 "+str(host)+" -c "+str(service_cmd) ) )
			else:
				print( doErrorHandle( str(service_cmd) ) )
			print(str(timestamp+" OK - Service "+str(service_name)+" restarted on host "+str(host_name)+"."))
#		else
#			print(str(timestamp+" OK - Service "+str(service_name)+" NOT restarted on host "+str(host_name)+"."))
	except Exception:
		print(str(" UNKNOWN - An error occured while handling the failure. Cascading failure."))
		exit(3)
	exit(0)


if __name__ == '__main__':
	main()

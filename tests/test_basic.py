# -*- coding: utf-8 -*-

import unittest
import subprocess

def getPythonCommand():
	"""function for backend python command"""
	thepython = "exit 1 ; #"
	try:
		import sys
		if sys.__name__ is None:
			raise ImportError("Failed to import system. WTF?!!")
		thepython = checkPythonCommand(["which", "coverage"])
		if (str("/coverage") in str(thepython)) and (sys.version_info >= (3, 3)):
			thepython = str("coverage run -p")
		else:
			thepython = checkPythonCommand(["which", "python3"])
			if (str("/python3") not in str(thepython)) or (sys.version_info <= (3, 2)):
				thepython = "python3"
	except Exception:
		thepython = "exit 1 ; #"
		try:
			thepython = checkPythonCommand(["which", "python"])
			if (str("/python") in str(thepython)):
				thepython = "python"
		except Exception:
			thepython = "exit 1 ; #"
	return str(thepython)


def checkPythonCommand(args=[None], stderr=None):
	"""function for backend subprocess check_output command"""
	theOutput = None
	try:
		if args is None or args is [None]:
			theOutput = subprocess.check_output(["exit 1 ; #"])
		else:
			if str("coverage ") in args[0]:
				args[0] = str("coverage")
				args.insert(1, str("run"))
				args.insert(2, str("-p"))
				args.insert(2, str("--source=code"))
			theOutput = subprocess.check_output(args, stderr=stderr)
	except Exception:
		theOutput = None
	if isinstance(theOutput, bytes):
		theOutput = theOutput.decode('utf8')
	return theOutput


class BasicTestSuite(unittest.TestCase):
	"""Basic test cases."""

	def test_absolute_truth_and_meaning(self):
		"""Insanitty Test."""
		assert True

	def test_syntax(self):
		"""Test case importing code."""
		theResult = False
		try:
			from .context import code
			from code import restart_service
			theResult = True
		except Exception:
			theResult = False
		assert theResult

	def test_a_which_command(self):
		"""Test case for backend which."""
		theResult = False
		try:
			import subprocess
			theOutputtext = subprocess.check_output(["which", "which"])
			try:
				if (str("/which") in str(theOutputtext)):
					theResult = True
			except Exception as err:
				print(err.msg)
		except Exception:
			theResult = False
		assert theResult

	def test_z_remote_command(self):
		"""Test case for backend library."""
		theResult = False
		try:
			import subprocess
			theOutputtext = subprocess.check_output(["which", "check_nrpe"])
			if (str("/check_nrpe") in str(theOutputtext)):
				theResult = True
		except Exception:
			theResult = False
			try:
				theOutputtext = subprocess.check_output(["which", "ssh"])
				if (str("/ssh") in str(theOutputtext)):
					theResult = True
			except Exception:
				theResult = False
		assert theResult

	def test_z_z_func_command_help(self):
		"""Test case for --help option."""
		theResult = False
		try:
			theOutputtext = checkPythonCommand([getPythonCommand(),
				str("code/restart_service.py"),
				str("--help")
			], stderr=subprocess.STDOUT)
			if (str("usage") in str(theOutputtext)):
				theResult = True
		except Exception:
			theResult = False
		assert theResult

	def test_z_z_func_command_local(self):
		"""Test case for --use-local option."""
		theResult = False
		try:
			theOutputtext = checkPythonCommand([getPythonCommand(),
				str("code/restart_service.py"),
				str("--use-local"),
				str("-E"),
				str("5"),
				str("CRITICAL"),
				str("HARD"),
				str("5"),
				str("localhost"),
				str("true"),
				str("\"test\"")
			], stderr=subprocess.STDOUT)
			if (str("OK - Service test restarted on host localhost") in str(theOutputtext)):
				theResult = True
			elif (str("OK - Service \"test\" restarted on host localhost") in str(theOutputtext)):
				theResult = True
			else:
				 print(str(theOutputtext))
		except Exception:
			theResult = False
		assert theResult

if __name__ == '__main__':
	unittest.main()
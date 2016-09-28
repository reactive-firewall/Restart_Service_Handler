# -*- coding: utf-8 -*-

import unittest


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
			if ("/which" in theOutputtext):
				theResult = True
		except Exception:
			theResult = False
		assert theResult

	def test_z_remote_command(self):
		"""Test case for backend library."""
		theResult = False
		try:
			import subprocess
			theOutputtext = subprocess.check_output(["which", "check_nrpe"])
			if ("/check_nrpe" in theOutputtext):
				theResult = True
		except Exception:
			theResult = False
			try:
				theOutputtext = subprocess.check_output(["which", "ssh"])
			except Exception:
				theResult = False
			if ("/ssh" in theOutputtext):
				theResult = True
		assert theResult

if __name__ == '__main__':
	unittest.main()
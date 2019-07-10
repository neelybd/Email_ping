import re
import smtplib
import dns.resolver
import pandas as pd
from tkinter import Tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from joblib import Parallel, delayed
import multiprocessing

def main():
	print("Program: Email Ping")
	print("Release: 1.0")
	print("Date: 2019-05-31")
	print("Author: Brian Neely")
	print()
	print()
	print("This program pings a email web server for a specified email address in a csv.")
	print("It assumes that the csv file is encoded in UTF-8 and is comma delimited.")
	print("A significant portion of the ping_email function is copied from the work of Scott Brady from his Python-Email-Verification-Script")
	print("His work and this work is licensed under the Apache License 2.0")
	print()
	print()

	print("Program Starting")
	# Hide Tkinter GUI
	Tk().withdraw()

	# Find input file
	print("Select File in")
	file_in = askopenfilename(initialdir="../", title="Select input file",
							  filetypes=(("Comma Separated Values", "*.csv"), ("all files", "*.*")))
	if not file_in:
		input("Program Terminated. Press Enter to continue...")
		exit()

	# Set ouput file
	file_out = asksaveasfilename(initialdir=file_in, title="Select output file",
								 filetypes=(("Comma Separated Values", "*.csv"), ("all files", "*.*")))
	if not file_out:
		input("Program Terminated. Press Enter to continue...")
		exit()

	# Read csv
	data = pd.read_csv(file_in, low_memory=False)

	# Find email column
	email_col = column_selection(list(data))

	# Test each email address
	email_list = Parallel(n_jobs=60)(delayed(ping)(i, index) for index, i in enumerate(data[email_col]))
	data["Email Validity"] = email_list

	# Write CSV
	print("Writing CSV File...")
	data.to_csv(file_out, index=False)
	print("Wrote CSV File!")
	print()

	print("File written to: " + file_out)
	input("Press Enter to close...")

def ping(i, index):
	# print('')
	if index % 100 == 0:
		print(str(index) + ": " + str(i))
	try:
		return ping_email(i)
	except:
		return "Domain Doesn't Exist"

def ping_email(inputAddress):
	try:
		# Print what email is being tested
		# print("Testing: " + inputAddress)

		# Address used for SMTP MAIL FROM command
		fromAddress = 'noresponse@gmail.com'

		# Simple Regex for syntax checking
		regex = '^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,})$'

		# Email address to verify
		addressToVerify = str(inputAddress)

		# Lower case address
		addressToVerify = addressToVerify.lower()

		# Syntax check
		match = re.match(regex, addressToVerify)
		if match == None:
			return 'Bad Syntax'

		# Get domain for DNS lookup
		splitAddress = addressToVerify.split('@')
		domain = str(splitAddress[1])
		# print('Domain:', domain)

		# MX record lookup
		records = dns.resolver.query(domain, 'MX')
		mxRecord = records[0].exchange
		mxRecord = str(mxRecord)

		# SMTP lib setup (use debug level for full output)
		server = smtplib.SMTP(timeout=360)
		server.set_debuglevel(0)

		# SMTP Conversation
		server.connect(mxRecord)
		server.helo(server.local_hostname) ### server.local_hostname(Get local server hostname)
		server.mail(fromAddress)
		code, message = server.rcpt(str(addressToVerify))
		server.quit()

		#print(code)
		#print(message)

		# Assume SMTP response 250 is success
		if code == 250:
			return 'Success'
		else:
			return 'Failed'
	except:
		return "Domain Doesn't Exist"


def column_selection(headers):
	while True:
		try:
			print("Select column.")
			for j, i in enumerate(headers):
				print(str(j) + ": to perform sentiment analysis on column [" + str(i) + "]")
			column = headers[int(input("Enter Selection: "))]
		except ValueError:
			print("Input must be integer between 0 and " + str(len(headers)))
			continue
		else:
			break
	return column


if __name__ == '__main__':
	main()

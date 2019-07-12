import pandas as pd
from tkinter import Tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from joblib import Parallel, delayed
from email_ping import *
from unknown_encoding import *
import multiprocessing

# Unknown Encoder Failure

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

	# Identify CSV Encoding
	# encoder = open_unknown_csv(file_in, ",")
	# if encoder == "Unknown":
	# 	encoder = encoding_selection("Encoder could not be Identified, please select encoding.")
	encoder = encoding_selection("Encoder could not be Identified, please select encoding.")

	# Read csv
	data = pd.read_csv(file_in, low_memory=False, encoding=encoder)

	# Find email column
	email_col = column_selection(list(data))

	# Test each email address
	email_list = Parallel(n_jobs=60)(delayed(ping, 10)(i, index) for index, i in enumerate(data[email_col]))
	data["Email Validity"] = email_list

	# Write CSV
	print("Writing CSV File...")
	data.to_csv(file_out, index=False)
	print("Wrote CSV File!")
	print()

	print("File written to: " + file_out)
	input("Press Enter to close...")

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

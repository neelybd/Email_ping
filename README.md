# Email_ping

This program pings a email web server for a specified email address in a csv.
  
It assumes that the csv file is encoded in UTF-8 and is comma delimited.

To use:
    Run either the py file or exe
    Select input csv file
    A list of columns will be displayed, select the desired column index to perform the email pings
    Select the output csv file
    Wait until the output file is written.

Note: The results of the ping will be written to a column named: "Email Validity". If this column already exists, any data there will be overwritten.

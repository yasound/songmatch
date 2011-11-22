#!/usr/bin/python
import psycopg2
import sys
import pprint

def main():
	#start the script

	conn_string = "host='yasound.com' port='5433' dbname='yasound' user='yasound' password='ufAHo10qAd0w'"
	# print the connection string we will use to connect
	print "Connecting to database\n	->%s" % (conn_string)
	try:
		# get a connection, if a connect cannot be made an exception will be raised here
		conn = psycopg2.connect(conn_string)

		# conn.cursor will return a cursor object, you can use this cursor to perform queries
		cursor = conn.cursor()

		# execute our Query
		cursor.execute("SELECT COUNT(name) FROM yasound_song")

		# retrieve the records from the database
		records = cursor.fetchall()

		# print out the records using pretty print
		# note that the NAMES of the columns are not shown, instead just indexes.
		# for most people this isn't very useful so we'll show you how to return
		# columns as a dictionary (hash) in the next example.
		pprint.pprint(records)
	except:
		# Get the most recent exception
		exceptionType, exceptionValue, exceptionTraceback = sys.exc_info()
		# Exit the script and print an error telling what happened.
		sys.exit("Database connection failed!\n ->%s" % (exceptionValue))


if __name__ == "__main__":
	sys.exit(main())


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

        # execute our 1st Query
        cursor.execute("SELECT COUNT(*) FROM yasound_song")
        records = cursor.fetchall()
        print str(records[0][0]) + " songs found"

        cursor.execute("SELECT COUNT(*) FROM yasound_artist")
        records = cursor.fetchall()
        print str(records[0][0]) + " artists found"

        cursor.execute("SELECT COUNT(*) FROM yasound_album")
        records = cursor.fetchall()
        print str(records[0][0]) + " albums found"


        # execute our 2nd Query
        #cursor.execute("SELECT name FROM yasound_song")
        records = cursor.fetchall()
        print str(len(records)) + " records found"
    except:
        # Get the most recent exception
        exceptionType, exceptionValue, exceptionTraceback = sys.exc_info()
        # Exit the script and print an error telling what happened.
        sys.exit("Database connection failed!\n ->%s" % (exceptionValue))


if __name__ == "__main__":
  	sys.exit(main())


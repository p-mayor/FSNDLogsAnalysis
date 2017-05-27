#!/usr/bin/env python

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    try:
        db = psycopg2.connect("dbname=news")
        cursor = db.cursor()
        return db, cursor
    except:
        print("failed to connect")

def close(db):
    db.commit()
    db.close()

def articleCount():
	db, cursor = connect()
	query = "select * from articlecount order by num desc limit 3"
	cursor.execute(query)
	results = cursor.fetchall()
	results_list = []
	for i in results:
		list_item = str(i[0]) + ' - ' + str(i[1]) + ' views'
		results_list.append(list_item)
	print 'Article Popularity:'
	print results_list
	close(db)

def authorCount():
	db, cursor = connect()
	query = "select * from authorcount order by sum desc"
	cursor.execute(query)
	results = cursor.fetchall()
	results_list= []
	for i in results:
		list_item = str(i[1]) + ' - ' + str(i[0]) + ' views'
		results_list.append(list_item)
	print 'Author Popularity:'
	print results_list
	close(db)

def errorDays():
	"""returns days in database with errors greater than 1%"""
	db, cursor = connect()
	query = "select * from err_days order by perc desc"
	cursor.execute(query)
	results = cursor.fetchall()
	day = results[0][1]
	err = results[0][0]
	output = day + ' - ' + str(err) + ' %'
	print 'Days with errors over 1%:'
	print output
	close(db)

connect()
articleCount()
authorCount()
errorDays()


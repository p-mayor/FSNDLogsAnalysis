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
	print("Most popular articles:")
	for (title, num) in results:
		print ("    {} - {} views".format(title, num))
	print ("-" * 70)
	close(db)


def authorCount():
	db, cursor = connect()
	query = "select * from authorcount order by sum desc"
	cursor.execute(query)
	results = cursor.fetchall()
	print ("Most popular authors:")
	for (name, sum) in results:
		print ("    {} - {} views".format(name, sum))
	print ("-" * 70)
	close(db)


def errorDays():
	"""returns days in database with errors greater than 1%"""
	db, cursor = connect()
	query = "select * from err_days order by perc desc"
	cursor.execute(query)
	results = cursor.fetchall()
	print 'Days with errors over 1%:'
	for (day, perc) in results:
		print ("    {} - {} percent".format(day, perc))
	print ("-" * 70)
	close(db)


connect()
articleCount()
authorCount()
errorDays()

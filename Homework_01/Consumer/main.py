import pika
import datetime
import sys
import psycopg2
import psycopg2.extras
import time

def db_init(cursor):
	cursor.execute('''
		CREATE TABLE IF NOT EXISTS 
		messages(id SERIAL PRIMARY KEY, 
			     message TEXT NOT NULL, 
		         timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL);''')

def db_insert(cursor, message):
	cursor.execute('''INSERT INTO messages (message) VALUES (%s);''', (message,))

try:
	# Connecting to Postgres
	retries = 3
	while retries > 0:
		try:		
			db_connection = psycopg2.connect(host="postgres", dbname="messages", user="user", password="password")
			break
		except Exception as e:
			time.sleep(10)
			retries -= 1
	if retries == 0:
		raise Exception("Unable to connect to postgress")

	db_connection.autocommit = True
	db_cursor = db_connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
	db_init(db_cursor)
	
	db_cursor.execute('''SELECT COUNT(*) as count FROM messages;''')
	messages_count = db_cursor.fetchone()["count"]

	print("Already {} messages are stored".format(messages_count))

	# Connecting to RabbitMq
	retries = 3
	while retries > 0:
		try:
			rabbit_connection = pika.BlockingConnection(
				pika.URLParameters("amqp://guest:guest@rabbitmq:5672") 
			)
			break
		except Exception as e:
			time.sleep(10)
			retries -= 1
	if retries == 0:
		raise Exception("Unable to connect to RabbitMQ")

	rabbit_channel = rabbit_connection.channel()
	rabbit_channel.queue_declare(queue='messages')
	
	# Starting the lifecycle
	print("Hrrrr, how I am ready to listen your messages...")
	sys.stdout.flush()
	def callback(ch, method, properties, body):	
		try:
			now_time = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")

			message = body.decode()
			db_insert(db_cursor, message)

			print("[{}] {}".format(now_time, message))
			sys.stdout.flush()
		except Exception as e:
			print(e)
			sys.stdout.flush()
	
	rabbit_channel.basic_consume(callback, queue='messages', no_ack=True)
	rabbit_channel.start_consuming()

except Exception as e:
	print(e)
	exit(1)
finally:
	db_cursor.close()
	db_connaction.close()
	
	rabbit_connection.stop()

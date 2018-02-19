import pika
import datetime
import sys

try:
	connection = pika.BlockingConnection(
		pika.URLParameters("amqp://guest:guest@rabbitmq:5672") 
	)
	channel = connection.channel()
	channel.queue_declare(queue='messages')
	
	print("Hrrrr, how I am ready to listen your messages...")
	def callback(ch, method, properties, body):	
		try:
			now_time = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
			print("[{}] {}".format(now_time, body.decode()))
			sys.stdout.flush()
		except Exception as e:
			print(e)
			sys.stdout.flush()
	
	channel.basic_consume(callback, queue='messages', no_ack=True)
	channel.start_consuming()

except Exception as e:
	print(e)
	exit(1)

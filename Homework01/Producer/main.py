import pika

print("Enter text to send it into queue:")

message = input()

try:
	connection = pika.BlockingConnection(pika.URLParameters("amqp://guest:guest@localhost:32769"))

	channel = connection.channel()
	channel.queue_declare(queue='message_queue') 
	channel.basic_publish(exchange='', routing_key='message_queue', body=message.encode())
except Exception as e:
	print(e)
	exit(1)

print("Message was succesfully queued")

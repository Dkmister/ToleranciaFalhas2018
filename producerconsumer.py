#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Codigo inspirado pelo site agiliq.com
from threading import Thread,Condition
import time
import random
import sys

queue = []
MAX_NUM = 1
condition = Condition()
output = []
output_str = ''
prod_total = 0
cons_total = 0
"""
classe Produtor :

metodo run:

Produz um item e coloca numa fila..

Utiliza condition para fazer sincronização e espera da outra thread Consumidor.

"""
class ProducerThread(Thread):
	def run(self):
		nums = range(5)
		global queue
		prod_total = 0
		while prod_total < 10:
			condition.acquire()
			if len(queue) == MAX_NUM:
				print ("Fila cheia, produtor esperando...")
				condition.wait()
				print ("Espaço na fila, Consumidor notificou o programa")
			num = random.choice(nums)
			queue.append(num)
			print ("Produzido: ")
			print (num)
			with open(output_filename, 'a') as file:
				file.write('Produzido 1\n')
			condition.notify()
			condition.release()
			time.sleep(random.random())
			prod_total += 1
"""
classe Consumidor:

metodo run:

Espera um item estar na fila construída pelo Produtor.

Utiliza sincronização e espera , através do condition para a correta utilização do algoritmo.

"""
class ConsumerThread(Thread):
	def run(self):
		global queue
		cons_total = 0	
		while cons_total < 10:
			condition.acquire()
			if not queue:
				print ("Nada na fila, consumidor esperando ...")
				condition.wait()
				print ("Produtor adicionou algo na fila e notificou consumidor")
			num = queue.pop(0)
			print ("Consumido: ")
			output.append(1)
			print(num)
			with open(output_filename, 'a') as file:
				file.write('Consumido 1\n')
			condition.notify()
			condition.release()
			time.sleep(random.random())
			cons_total += 1

			

output_filename = str(sys.argv[1])
with open(output_filename, 'w') as file:
	file.write('Iniciando\n')
ProducerThread().start()
ConsumerThread().start()

	


#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Codigo inspirado pelo site agiliq.com
from threading import Thread,Condition
import time
import random

queue = []
MAX_NUM = 10
condition = Condition()
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
		while True:
			condition.acquire()
			if len(queue) == MAX_NUM:
				print ("Fila cheia, produtor esperando...")
				condition.wait()
				print ("Espaço na fila, Consumidor notificou o programa")
			num = random.choice(nums)
			queue.append(num)
			print ("Produzido: ")
			print (num)
			condition.notify()
			condition.release()
			time.sleep(random.random())
"""
classe Consumidor:

metodo run:

Espera um item estar na fila construída pelo Produtor.

Utiliza sincronização e espera , através do condition para a correta utilização do algoritmo.

"""
class ConsumerThread(Thread):
	def run(self):
		global queue
		while True:
			condition.acquire()
			if not queue:
				print ("Nada na fila, consumidor esperando ...")
				condition.wait()
				print ("Produtor adicionou algo na fila e notificou consumidor")
			num = queue.pop(0)
			print ("Consumido: ")
			print(num)
			condition.notify()
			condition.release()
			time.sleep(random.random())
			
			
			
ProducerThread().start()
ConsumerThread().start()

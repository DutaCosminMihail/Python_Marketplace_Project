"""
This module represents the Marketplace.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

from threading import Lock, currentThread
import time
import logging
from logging.handlers import RotatingFileHandler

class Marketplace:
    """
    Class that represents the Marketplace. It's the central part of the implementation.
    The producers and consumers use its methods concurrently.
    """
    def __init__(self, queue_size_per_producer):
        """
        Constructor

        :type queue_size_per_producer: Int
        :param queue_size_per_producer: the maximum size of a queue associated with each producer
        """

        #queue_size_per_producer -> dim maxima a unei cozi asociate fiecarui producer
        #lock-urile sunt folosite peantru a sinconiza accesul la structurile de date partajate


        self.handler = RotatingFileHandler('./marketplace.log', maxBytes=15000, backupCount=40)
        logging.basicConfig(handlers=[self.handler],
                            format='%(asctime)s %(levelname)s:%(message)s',
                            level=logging.INFO)
        logging.Formatter.converter = time.gmtime

        self.queue_size_per_producer = queue_size_per_producer
        self.carts = {}
        self.producers = {}
        self.products_in_carts = {}
        self.counter_products = 0
        self.counter_consumers = 0

        self.queue_lock = Lock()
        self.number_carts_lock = Lock()
        self.register_producer_lock = Lock()
        self.print_lock = Lock()

    def register_producer(self):
        """
        Returns an id for the producer that calls this.
        """
        #metoda utilizata pentru a inregistra un producator
        #metoda returneaza un ID pentru fiecare producator

        logging.info("INFO: Check for the register_producer:")
        try:
            self.register_producer_lock.acquire()
            producer_id = len(self.producers)
            self.producers[producer_id] = []
            self.products_in_carts[producer_id] = []
            return producer_id
        finally:
            self.register_producer_lock.release()
            logging.info("INFO: Producer %d is already checked as being registered!", producer_id)

    def publish(self, producer_id, product):
        """
        Adds the product provided by the producer to the marketplace

        :type producer_id: String
        :param producer_id: producer id

        :type product: Product
        :param product: the Product that will be published in the Marketplace

        :returns True or False. If the caller receives False, it should wait and then try again.
        """
        #metoda introduce in marketplace un produs de un producator
        #returnez True => daca produsul este adaugat cu success pe piata
        #returnez False => caz contrar (se asteapta si dupa se incearca iar)
        logging.info("INFO: Producer %d attempted to publish the product %s.", producer_id, product)
        producer_queue = self.producers.get(producer_id)
        queue_size_per_producer_instance = self.queue_size_per_producer

        try:
            if len(producer_queue) >= queue_size_per_producer_instance:
                logging.warning("WARNING: Producer %d queue is already full!", producer_id)
                return False
            self.producers[producer_id].append(product)
            logging.info("INFO: Producer %d successfully managed to publish the product %s.",
                         producer_id, product)
            return True
        except KeyError:
            return False

    def new_cart(self):
        """
        Creates a new cart for the consumer

        :returns an int representing the cart_id
        """
        #lock -> ma asigur ca un singur consumator poate crea un cos la un moment dat
        #aloc un ID unic noului cart (valoarea counter_consumers - nr. de consumatori)
        # initializez lista goala pt continutul cart ului si adaug cart ul in dictionar
        #dictionarul are cheia cart_id
        #la final incrementez counterul pentru a ma asigura ca urmatorul cart este creat
        #si are un ID unic la randul sau
        logging.info("INFO: Consumer desires to attempt to create a new cart")
        try:
            self.number_carts_lock.acquire()
            cart_id = self.counter_consumers
            self.carts[cart_id] = []
            self.counter_consumers += 1
        finally:
            self.number_carts_lock.release()

        logging.info("INFO: Cart is %d successfully created!", cart_id)
        return cart_id

    def find_product(self, product, place):
        for i in range(len(place)):
            for j in place[i]:
                if j == product:
                    return i
        return None

    def add_to_cart(self, cart_id, product):
        """
        Adds a product to the given cart. The method returns

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to add to cart

        :returns True or False. If the caller receives False, it should wait and then try again
        """

        logging.info("INFO: Trying to add the product %s to the cart %d", product, cart_id)
        #apelez find_product pt a gasi producatorul produsului
        #in caz contrar => return False
        #elimin produsul din lista de produse disponibile a producatorului
        #adaug produsul la lista de produse din cart
        #adaug produsul in cart ul consumatorului adaugandu-l la lista de produse din acel cart
        try:
            producer = self.find_product(product, self.producers)
            if producer is None:
                logging.warning("WARNING: The product %s unfortunately cannot be found", product)
                return False
            self.queue_lock.acquire()
            try:
                self.producers[producer].remove(product)
                self.products_in_carts[producer].append(product)
                self.carts[cart_id].append(product)
            finally:
                self.queue_lock.release()

            logging.info("INFO: Product is %s added successfully to the cart %d", product, cart_id)
            return True
        except Exception as e:
            logging.error("ERROR: An exception occurred while adding product %s to cart %d: %s",
                          product, cart_id, str(e))
            return False

    def remove_from_cart(self, cart_id, product):

        """
        Removes a product from cart.

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to remove from cart
        """
        #verificam mai intai daca produsul este in cart
        #daca se gaseste => gasim producatorul cu ajutorul functiei find_product
        #il elimin din cos iar intrarile sunt actualizate in dictionarele respective
        #(products_in_carts/carts)
        try:

            if product in self.carts[cart_id]:
                producer = self.find_product(product, self.products_in_carts)
                self.carts[cart_id].remove(product)
                self.products_in_carts[producer].remove(product)
                self.producers[producer].append(product)
                logging.info("INFO: Cart is now %d removed  successfully from the cart %s",
                             cart_id, product)
                return True
            else:
                logging.warning("WARNING:Cart %d error!", cart_id)
                return False
        finally:
            pass

    def place_order(self, cart_id):
        """
        Return a list with all the products in the cart.

        :type cart_id: Int
        :param cart_id: id cart
        """
    #returnam lista de produse continute in cart avand cart_id ul respectiv
        logging.info("INFO: The order %d now is successfully placed - ENJOY!", cart_id)
        return self.carts[cart_id]

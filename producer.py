"""
This module represents the Producer.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

from time import sleep
from threading import Thread


class Producer(Thread):
    """
    Class that represents a producer.
    """

    def __init__(self, products, marketplace, republish_wait_time, **kwargs):
        """
        Constructor.

        @type products: List()
        @param products: a list of products that the producer will produce

        @type marketplace: Marketplace
        @param marketplace: a reference to the marketplace

        @type republish_wait_time: Time
        @param republish_wait_time: the number of seconds that a producer must
        wait until the marketplace becomes available

        @type kwargs:
        @param kwargs: other arguments that are passed to the Thread's __init__()
        """

        Thread.__init__(self, **kwargs)

        self.products = products
        self.marketplace = marketplace
        self.republish_wait_time = republish_wait_time
        #returnam ID-ul
        self.prod_id = self.marketplace.register_producer()

# (product , quantity, wait_time) - acestia sunt parametrii json-ului
#def run -> contine un loop care itereaza peste o lista de produse (fiecare
# fiind reprezentat ca o lista de 3 param: produs, cantitate si timpul de asteptare)
#al doilea loop se exec pana cand produsul se executa cu succes (folosindu-ne de ID)
#True => bucla se intrerupe si se asteapta timpul specificat
#False => se asteapta pentru republicare inainte de publicarea din nou a produsului
# i => index pt nr.de produse

    def run(self):
        while True:
            for products_json_parameters in self.products:
                #parameters
                product = products_json_parameters[0]
                quantity = products_json_parameters[1]
                wait_time = products_json_parameters[2]
                i = 0
                while i < quantity: #pentru fiecare product quantity
                    while True:
                        product_publish = self.marketplace.publish(self.prod_id, product)

                        if product_publish:
                            break
                        sleep(self.republish_wait_time)
                        product_publish = self.marketplace.publish(self.prod_id, product)

                    sleep(wait_time) #asteptam produsul
                    i += 1

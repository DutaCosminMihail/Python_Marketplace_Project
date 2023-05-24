"""
This module represents the Consumer.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

from threading import Thread
import time


class Consumer(Thread):
    """
    Class that represents a consumer.
    """

    def __init__(self, carts, marketplace, retry_wait_time, **kwargs):
        """
        Constructor.

        :type carts: List
        :param carts: a list of add and remove operations

        :type marketplace: Marketplace
        :param marketplace: a reference to the marketplace

        :type retry_wait_time: Time
        :param retry_wait_time: the number of seconds that a producer must wait
        until the Marketplace becomes available

        :type kwargs:
        :param kwargs: other arguments that are passed to the Thread's __init__()
        """
        Thread.__init__(self, **kwargs)

        self.carts = carts
        self. marketplace = marketplace
        self.retry_wait_time = retry_wait_time

# primul loop - iterez peste o lista de buckets/carts
#pt fiecare bucket  => consumer ul creeaza un cos nou folosind new_cart
# urmatorul loop - iterez peste operatiile din bucket-ul curent si pentru
#fiecare operatie se preia tipul operatiie, produsul si cantitatea
#urmatoarul loop - in functie de cantitate se executa operatia curenta de mai multe ori
#(add_to_cart/remove_from/cart) pana cand e successfull operatiunea
#duoa ce toate operatiile din cos au fost executate cu success, metoda apeleaza
#place_order (folosindu-ne de cart_id) pentru a cumpara produsele din cos
#bloc try-finally -> pentru a asigura corectitudine si pentru a ne aigura
#ca mai multe fire de executie nu ruleaza in acelasi timp

    def run(self):
        for cart in self.carts:
            cart_id = self.marketplace.new_cart()
            for oper in cart:
                op_type = oper["type"]
                op_product = oper["product"]
                op_quantity = oper["quantity"]

                for i in range(op_quantity):
                    success = False

                    while not success:
                        if op_type == "add":
                            success = self.marketplace.add_to_cart(cart_id, op_product)
                        else:
                            success = self.marketplace.remove_from_cart(cart_id, op_product)

                        if success:
                            i += 1
                        else:
                            time.sleep(self.retry_wait_time)

            cart_contents = self.marketplace.place_order(cart_id)
            try:
                self.marketplace.print_lock.acquire()

                for product in cart_contents:
                    print(f"{self.name} bought {product}")
            finally:
                self.marketplace.print_lock.release()
                
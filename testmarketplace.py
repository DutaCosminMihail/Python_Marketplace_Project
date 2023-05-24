import unittest
from marketplace import Marketplace

class TestMarketplace(unittest.TestCase):
    REGISTER_LENGTH = 10
    PRODUCT_LENGTH = 3

    def setUp(self):
        self.marketplace = Marketplace(self.PRODUCT_LENGTH)

    def test_register_product(self):
        i = 0
        try:
            while i < self.REGISTER_LENGTH:
                producer_id = self.marketplace.register_producer()
                expected_id = i
                assert producer_id == expected_id, f"It's an unexpected producer id: {producer_id}. It's an expected: {expected_id}"
                i += 1
        finally:
            print("Test_register_product final unit check: PASSED")

    def test_publish(self):
        producer_id = self.marketplace.register_producer()
        i = 0
        try:
            while True:
                product = f"Product {i}"
                assert self.marketplace.publish(producer_id, product), f"Unfortunate failure to publish the product {product}"
                i += 1
        except AssertionError:
            product = f"Product {i}"
            assert not self.marketplace.publish(producer_id, product), f"Successful publish of the product {product} above maximum limit"
        finally:
            print("Test_publish final unit check: PASSED")

    def test_new_cart(self):
        i = 0
        try:
            while i < self.REGISTER_LENGTH:
                cart_id = self.marketplace.new_cart()
                assert cart_id == i, f"It's an unexpected cart ID: {cart_id}. It's one expected: {i}"
                i += 1
        finally:
            print("Test_new_cart final unit check: PASSED")

    def test_add_to_cart(self):
        producer_id = self.marketplace.register_producer()

        try:
            i = 0
            while i < self.PRODUCT_LENGTH:
                product = f"Product {i}"
                self.marketplace.publish(producer_id, product)
                i += 1

            cart_id = self.marketplace.new_cart()

            i = 0
            while i < self.PRODUCT_LENGTH:
                product = f"Product {i}"
                assert self.marketplace.add_to_cart(cart_id, product), f"Unfortunate failure to add the product {product} to the cart"
                i += 1
            product = f"Product {self.PRODUCT_LENGTH}"
            assert not self.marketplace.add_to_cart(cart_id, product), f"SUccessful attempt to add the product {product} above the maximum limit"
            product = "Product 0"
            assert not self.marketplace.add_to_cart(cart_id, product), f"Successful attempt to add the product {product} but it's already in the cart"
        finally:
            print("Test_add_to_the_cart final unit check: PASSED")

    def test_remove_from_cart(self):
        producer_id = self.marketplace.register_producer()

        try:
            i = 0
            while i < self.PRODUCT_LENGTH:
                product = f"Product {i}"
                self.marketplace.publish(producer_id, product)
                i += 1
            cart_id = self.marketplace.new_cart()

            product = f"Product {self.PRODUCT_LENGTH}"
            self.assertFalse(self.marketplace.remove_from_cart(cart_id, product))

            i = 0
            while i < self.PRODUCT_LENGTH:
                product = f"Product {i}"
                self.marketplace.add_to_cart(cart_id, product)
                i += 1

            i = 0
            while i < self.PRODUCT_LENGTH:
                product = f"Product {i}"
                self.assertTrue(self.marketplace.remove_from_cart(cart_id, product))
                i += 1
        finally:
            print("Remove_from_the_cart final unit check: PASSED")

    def test_place_order(self):
        producer_id = self.marketplace.register_producer()

        i = 0
        while i < self.PRODUCT_LENGTH:
            product = f"Product {i}"
            self.marketplace.publish(producer_id, product)
            i += 1

        cart_id = self.marketplace.new_cart()
        i = 0
        while i < self.PRODUCT_LENGTH:
            product = f"Product {i}"
            self.marketplace.add_to_cart(cart_id, product)
            i += 1

        try:
            result = self.marketplace.place_order(cart_id)
            expected_result = ["Product 0", "Product 1", "Product 2"]
            i = 0
            while i < len(expected_result):
                self.assertEqual(result[i], expected_result[i])
                i += 1
        except Exception as e:
            print("Unfortuante failure to place the specific order:", e)
        else:
            print("Test_place_order final unit check: PASSED")


if __name__ == '__main__':
    unittest.main()
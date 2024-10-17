import threading
import time
import random

class BarberShop:
    def __init__(self, num_chairs, total_customers):
        self.num_chairs = num_chairs
        self.total_customers = total_customers
        self.customers_served = 0
        self.waiting_customers = 0
        self.shop_open = True
        self.barber_ready = threading.Condition()
        self.customer_ready = threading.Condition()

    def open_shop(self):
        print("The barber shop is now open.")
        barber_thread = threading.Thread(target=self.barber)
        barber_thread.start()

    def barber(self):
        while True:
            with self.customer_ready:
                while self.waiting_customers == 0:
                    if not self.shop_open:
                        print("The barber shop is closing. No more customers.")
                        return  # Exit when shop is closed and no customers remain
                    print("The barber is sleeping...")
                    self.customer_ready.wait()  # Wait for a customer to arrive

                # A customer is ready for a haircut
                self.waiting_customers -= 1
                print("The barber starts cutting hair.")

            # Simulate hair cutting (release the lock before sleeping)
            time.sleep(random.randint(1, 3))

            with self.barber_ready:
                self.barber_ready.notify()  # Notify a customer that the barber is done
                print("The barber finished cutting hair.")
            
            with self.customer_ready:
                self.customers_served += 1
                if self.customers_served == self.total_customers:
                    self.shop_open = False  # Close the shop when all customers are served

    def customer(self, customer_id):
        with self.customer_ready:
            if self.waiting_customers < self.num_chairs:
                self.waiting_customers += 1
                print(f"Customer {customer_id} is waiting. Total waiting customers: {self.waiting_customers}")
                self.customer_ready.notify()  # Notify the barber that a customer is ready
            else:
                print(f"Customer {customer_id} left as there are no free chairs.")
                return  # Customer leaves if no chair is available

        # Wait for the barber to be ready
        with self.barber_ready:
            self.barber_ready.wait()  # Wait until the barber is ready
            print(f"Customer {customer_id} is getting a haircut.")

def main():
    num_chairs = 3  # Number of waiting chairs in the barber shop
    total_customers = 10  # Total number of customers to be served
    barber_shop = BarberShop(num_chairs, total_customers)
    barber_shop.open_shop()

    # Simulate customers arriving at random intervals
    for customer_id in range(1, total_customers + 1):
        customer_thread = threading.Thread(target=barber_shop.customer, args=(customer_id,))
        customer_thread.start()
        time.sleep(random.randint(1, 2))  # Customers arrive every 1-2 seconds

if __name__ == "__main__":
    main()

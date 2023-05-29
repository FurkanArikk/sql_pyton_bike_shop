from datetime import datetime
import random
import time
import sqlite3

class Database():
    def __init__(self):
        self.connect_database()

    def connect_database(self):
        self.con = sqlite3.connect("bike_shop.db")
        self.cursor = self.con.cursor()

        self.cursor.execute(
            "Create Table If Not Exists products (id Integer Primary Key, name TEXT, type TEXT, stock INT, rental_price INT, price INT)"
        )

        self.cursor.execute(
            "Create Table If Not Exists order_history (id Integer Primary Key, bike_id INT, order_type TEXT, order_time TEXT,name TEXT,type TEXT, piece INT, unit_price INT, total_price INT)"
        )
        self.con.commit()

    def get_latest_id(self, table_name):
        self.cursor.execute(f"Select Max(id) From {table_name}")
        self.latest_id = self.cursor.fetchall()[0][0]
        return self.latest_id

class Shop(Database):
    def __init__(self,name):
        super().__init__()
        self.name = name

    def welcome(self, ):
        #printing bikes to screen
        welcome_message = f"Welcome To {self.name}'s Bike Shop"
        print(welcome_message)

        while True:
            self.cursor.execute("SELECT * FROM products")
            all_products = self.cursor.fetchall()
            convert_all_str = lambda i: [str(j) for j in i]

            title = "NO  |--ID--|  |--NAME--|  |--TYPE--|  |--STOCK--|  |--RENTAL_PRICE--| |--PRICE--|"
            print("-" * len(title))
            print(title)
            print("-" * len(title))
            
            for i, j in enumerate(all_products, start=1):
                product_info = "{:<4}|{:<6}|{:<14}|{:<13}|{:<8}|{:<14}|{:<8}".format(i, *j)
                print(product_info)

            print("-" * len(title))
            return all_products

    def add_products(self, data_type, t1, t2, t3, text):
           # adding values to database by their variable type
           if data_type == "string":
               while True:
                   product_value = input(text).title()

                   if product_value == t1 or product_value == t2 or product_value == t3:
                       break
                   else:
                       print("Invalid Value,Please enter an valid value...")
                       continue
               return product_value

           elif data_type == "integer":
               while True:
                   try:
                       product_value = int(input(text))

                       if product_value < 0:
                           print("Please enter a valid value...")
                           continue
                       break
                   except ValueError:
                       print("\033[31mYou entered invalid value. Please enter integer number\033[31m")

               return product_value

    def add_random_product(self):
        # adding values randomly to table by given values
        names = ["Tornado", "Thunderbolt", "Velocity", "Aurora", "Phoenix", "Eclipse"]
        types = ["Daily Life", "Race", "Mountain"]
        stock = [10, 15, 20, 25, 30, 35, 40, 45, 50, 55]
        rental_prices = [9, 15, 20, 25, 30, 35]
        prices = [99, 149, 199, 249, 299, 349, 399, 449]
        
        existing_products = self.cursor.execute("SELECT name FROM products").fetchall()
        existing_product_names = [product[0] for product in existing_products]
        
        for i in range(6):
            random_name = random.choice(names)
            
            if random_name not in existing_product_names:
                self.cursor.execute("INSERT INTO products (name, type, stock, rental_price, price) VALUES (?, ?, ?, ?, ?)",
                                    (random_name, random.choice(types), random.choice(stock),
                                    random.choice(rental_prices), random.choice(prices)))
                existing_product_names.append(random_name)
        
        self.con.commit()


    def get_info(self, info_name, info_id, table_name):
        self.cursor.execute(f"Select {info_name} From {table_name} Where id = ?", (info_id,))
        result = self.cursor.fetchall()[0][0]
        return result

    def update_info(self, info_type, info_name, info_id, table_name, new_value):
        if info_type == "integer":
            self.cursor.execute(f"UPDATE {table_name} SET {info_name} = {new_value} WHERE id = ?", (info_id,))
        elif info_type == "string":
            self.cursor.execute(f"UPDATE {table_name} SET {info_name} = '{new_value}' WHERE id = ?", (info_id,))

        self.con.commit()        

class Money(Database):
    CURRENCY = "TRY"

    TRY_BANKNOTE = {
        "200 TRY":200,
        "100 TRY":100,
        "50 TRY":50,
        "20 TRY":20,
        "10 TRY":10,
        "5 TRY":5,
        "1 TRY":5
    }
    def __init__(self):
        self.money_received = 0
        self.profit = 0
        super().__init__()

    def payment(self, cost):
        for banknote in self.TRY_BANKNOTE:
            number_of_money = round(cost / self.TRY_BANKNOTE[banknote])

            if number_of_money > 0:
                print("-"*40)
                while True:
                    try:
                        money_received = int(
                            input(f"(You can pay with {number_of_money} banknotes)\nHow many {banknote} ?: ")) * \
                                         self.TRY_BANKNOTE[banknote]
                        if money_received < 0:
                            print("\033[31mYou can't enter value less than zero!\033[m")
                            continue
                        break
                    except ValueError:
                        print("\033[31mYour choice must be integer number!\033[m")

                self.money_received += money_received
                cost -= money_received

        return self.money_received

    def bill(self, cost):
        self.payment(cost)
        if self.money_received >= cost:
            change = round(self.money_received - cost, 2)
            print(f"\033[93mHere is {change:,.2f} {self.CURRENCY} in change.\033[m")
            self.profit += cost
            self.money_received = 0
            return True
        else:
            print("\033[33mThat's not enough!\033[m")
            self.money_received = 0
            return False

class Order_history(Database):
    def __init__(self):
        super().__init__()

    def show_order_history(self):
        while True:
            self.cursor.execute("Select id,bike_id,order_type,order_time,name,type,piece,unit_price,total_price From order_history")
            all_products = self.cursor.fetchall()
            title = "|--ORDER ID--|  |--BIKE ID--| |--ORDER TYPE--|  |--ORDER TIME--|  |--NAME--|  |--TYPE--|  |--PIECE--| |--UNIT PRICE--|  |--TOTAL PRICE--|"
            print("-" * len(title))
            print(title)
            for i in all_products:
                print(" {}".format("           ".join(map(str, i))))

            print("-" * len(title))
            return all_products

    def show_order_details(self, id, id_type):
        forewords = [
            "Order ID: ",
            "Bike ID: ",-
            "Order type: ",
            "Order time: ",
            "Bike name: ",
            "Type of bike: ",
            "Number of pieces: ",
            "Unit price: ",
            "Total price: ",
        ]
        if id_type == "Order ID":
            self.cursor.execute("Select * From order_history Where id = ?", (id,))

        elif id_type == "Bike ID":
            self.cursor.execute("Select * From order_history Where bike_id = ?", (id,))

        values = list(self.cursor.fetchone())
        for i in range(len(values)):
            print(f"{i + 1} - {forewords[i]}{values[i]}")     


database = Database()
bike_shop = Shop("Furkan")
money = Money()
order_history = Order_history()

while True:
    bike_shop.add_random_product()
    if not bike_shop.welcome():
         print("\033[33mThere is no product in our shop. Would you like to add some ? (Yes/No)\033[m")
         while True:
            answer = input("Enter your answer: ")
            if answer.lower().capitalize == "No":
                print("Have a great day...")
                break

            if answer.lower().capitalize() == "Yes":
                product_name = input("Enter the name of the product: ")
                product_type = bike_shop.add_product(
                        data_type="string",
                        t1="Daily Life",
                        t2="Race",
                        t3="Mountain",
                        text="Enter the type of the product (Daily Life/Race/Mountain): "
                )

                product_stock = bike_shop.add_products(
                        data_type="integer",
                        t1=None,
                        t2=None,
                        t3=None,
                        text="Enter the stock quantity of the product: "
                )
                product_rental_cost = bike_shop.add_products(
                        data_type="integer",
                        t1=None,
                        t2=None,
                        t3=None,
                        text="Enter the rental price of the product: "
                )
                product_cost = bike_shop.add_products(
                        data_type="integer",
                        t1=None,
                        t2=None,
                        t3=None,
                        text="Enter the price of the product: "
                )
                database.cursor.execute(
                    "Insert Into products ('name','type',stock,rental_price,price) Values (?,?,?,?,?)",
                    (product_name, product_type, product_stock, product_cost, product_rental_cost,))
                database.con.commit()
                print(f"\033[1;32mThe registration of the product named {product_name} has been successfully completed.\033[m")

            else:
                print("Invalid answer, Please try again...")
                continue
            break
    print('''                  
        **************************************** 
        |                                      |
        |    Please choose an option:          |
        |    1 - Buy Bike                      |
        |    2 - Rent Bike                     | 
        |    3 - Show My Order History         |
        |    Write 'Exit' to close the program |
        |                                      |
        ****************************************
    ''')
    choice = input("Enter your choice: ").lower().strip()
    
    if choice == "1":
        while True:
            try:
                bike_id = int(input("Enter the ID of the product you want: "))
                if bike_id > database.get_latest_id("products") or bike_id <= 0:
                    print("\033[31mPlease choose an available option!\033[m")
                break
            except ValueError:
                print("\033[31mInvalid value!\033[m")

        stock_info = bike_shop.get_info(info_name="stock", info_id=bike_id, table_name="products")
        price_info = bike_shop.get_info(info_name="price", info_id=bike_id, table_name="products")
        name_info = bike_shop.get_info(info_name="name", info_id=bike_id, table_name="products")
        type_info = bike_shop.get_info(info_name="type", info_id=bike_id, table_name="products")
        rental_price_info = bike_shop.get_info(info_name="rental_price", info_id=bike_id, table_name="products")    

        while True:
            try:
                print(f"Current stock is: {stock_info}")
                how_many = int(input("How many bikes would you like to buy? "))
                
                if how_many > stock_info:
                    print("\033[31mYou can't buy more than the current stock!\033[m")
                    continue
                if how_many == 0:
                    print("You're returning to the main menu...")
                    time.sleep(2)
                break
            except ValueError:
                print("\033[31mYour choice must be an integer. Please write in the correct format!\033[m")

        total_cost = price_info * how_many
        total_cost_blue = f"\033[34m{total_cost:,.2f}\033[34m"
        print(f"{how_many} {name_info} cost {total_cost_blue} {money.CURRENCY}")
        sufficient_money = money.payment(total_cost)

        if sufficient_money and stock_info >= how_many:
            print("\033[32mWe are preparing your bike now. Please wait.\033[m")
            time.sleep(2)

            print("-" * 40)
            print("\033[32mYour order has been shipped.\033[m")
            print("-" * 40)                
            print("-" * 40)
            day = random.choice(range(6))
            print(f"\033[93mYour order will be ready in {day} day.\033[m")
            print("-" * 40)

            # Updating stocks
            updated_stock = stock_info - how_many
            bike_shop.update_any_info(
                info_type="integer", info_name="stock", info_id=bike_id, table_name="products", new_value=updated_stock)
            
            # Taking order time
            today = datetime.datetime.today()
            today_format = today.strftime("%d/%m/%Y %H:%M:%S")
            database.cursor.execute(
                "INSERT INTO order_history (bike_id, 'order_typ', 'order_time', 'name', 'typ', piece, unit_price, total_price) VALUES (?,?,?,?,?,?,?,?)",
                (bike_id, "Purchase", today_format, name_info, type_info, how_many, price_info, total_cost))
            database.con.commit()

            print("\033[32mThank you for choosing us!\033[m")
            choice2 = input("Press Enter to continue: ")
            print("-" * 60)
            continue

    if choice == "2":
            while True:
                try:
                    bike_id = int(input("Enter ID of product that you want to rent: "))
                    if bike_id > database.get_latest_id("products") or bike_id <= 0:
                        print("\033[31mError. Please choose an available option.\033[m")
                    break
                except ValueError:
                        print("\033[31mError. You entered invalid value\033[m")    

            
            stock_info = bike_shop.get_info(info_name="stock", info_id=bike_id, table_name="products")
            price_info = bike_shop.get_info(info_name="price", info_id=bike_id, table_name="products")
            name_info = bike_shop.get_info(info_name="name", info_id=bike_id, table_name="products")
            typ_info = bike_shop.get_info(info_name="type", info_id=bike_id, table_name="products")
            rental_price_info = bike_shop.get_info(info_name="rental_price", info_id=bike_id, table_name="products")    

            while True:
                try:
                    print(f"\033[93mCurrent stock is : {stock_info}\033[m")
                    how_many = int(input("How many bikes would you like to rent ?: "))
                    if how_many > stock_info:
                        print("\033[31mWe dont have enough bike to rent, Please enter an avaibale option\033[31m")
                        continue
                    if how_many == 0:
                        print("\033[31mYou didnt rent any bike,going back to maain menu\033[31m")
                        time.sleep(2)
                    break
                except ValueError:
                    print("\033[31mPlease enter an integer value!\033[31m")
           
            while True:
                rent_type  = input("Whic rental type would you like to use.(Hourly / Daily)").lower().capitalize()

                if rent_type == "Hourly":
                    order_type = "Rent(Hourly)"
                    total_rent_cost = (price_info * how_many)/200
                    total_rent_cost_yellow = f"\033[93m{total_rent_cost}\033[m"
                    print(f"{how_many} {name_info} cost {total_rent_cost_yellow} {money.CURRENCY} per hour")
                    break
                elif rent_type == "Daily":
                    order_type = "Rent(Daily)"
                    total_rent_cost = (price_info * how_many) / 250
                    total_rent_cost_yellow = f"\033[93m{(total_rent_cost * 24)}\033[m"
                    print(f"{how_many} {name_info} cost {total_rent_cost_yellow} {money.CURRENCY} per day")
                    break
                else:
                    print("\033[31mPlease choose an available options\033[31m")

            print("Your order has been preparing, Please wait")
            time.sleep(2)
            print("-"*40)
            print("\033[32mYour bike is ready.\033[m")
            print("-"*40)
            print("-"*40)
            print("\033[32mYou will pay, when you return the bike.\033[m")
            print("-"*40)
            print("-"*40)
            print("For more information, you can visit 'Show My Order History' section.")
            print("-"*40)

            #updating stocks
            updated_stock = stock_info - how_many
            bike_shop.update_info(
                info_type="integer", info_name="stock", info_id=bike_id, table_name="products", new_value=updated_stock
            )
            #recording time
            today = datetime.today()
            today_format = today.strftime("%d/%m/%Y %H:%M:%S")

            database.cursor.execute(
            "INSERT INTO order_history (bike_id, 'order_type', 'order_time', 'name', 'type', piece, unit_price, total_price) VALUES (?,?,?,?,?,?,?,?)",
            (bike_id, order_type, today_format, name_info, typ_info, how_many, price_info, total_rent_cost))
            database.con.commit()

            print("\033[32mThank you for choosing us\033[m")
            choice3 = input("Press enter any value to continue: ")
            print("-" * 50)
            continue

    if choice == "3":
                print("-" * 20)
                print("\033[95mYOUR ORDER HISTORY: \033[m")
                print("-" * 20)
                print("\033[93mYyou can find all information about your orders.\033[m")
                print("\033[93mEnter 'ORDER ID' of order history that you want to see more detailed.\033[m")

                if not order_history.show_order_history():
                    print(("*" * 45).center(90))
                    print("You didn't buy anything yet.".center(90))
                    print("Let's go to the main page,".center(90))
                    print(("*" * 45).center(90))

                while True:
                    try:
                        choice = int(input("Enter the Order Id to see your history.(Enter '0' to go back to main menu)"))
                        if choice == 0:
                            break
                        if choice > database.get_latest_id("order_history") or choice < 0:
                            print("\033[31mPlease choose an available option.\033[m")
                            continue
                        print("-"*50)
                        order_history.show_order_details(id_type="Order ID", id=choice)
                        print("-"*50)
                        while True:
                            print("\033[93mWhat would you like to do ?\n\033[m"
                                  "1 - Return my bike( Only for purchased bikes )\n"
                                  "2 - Pay for the bike( Only for rented bikes )\n"
                                  "3 - Exit\n")
                            choice1 = input("Enter your choice: ")
                            order_info = bike_shop.get_info(info_name="order_type", info_id=choice, table_name="order_history")
                            stock_info = bike_shop.get_info(info_name="stock", info_id=bike_id, table_name="order_history")
                            price_info = bike_shop.get_info(info_name="price", info_id=bike_id, table_name="order_history")
                            name_info = bike_shop.get_info(info_name="name", info_id=bike_id, table_name="order_history")
                            typ_info = bike_shop.get_info(info_name="type", info_id=bike_id, table_name="order_history")
                            piece_info = bike_shop.get_info(info_name="piece", info_id=choice, table_name="order_history")
                            rental_price_info = bike_shop.get_info(info_name="rental_price", info_id=bike_id, table_name="order_history")
                            total_price_info = bike_shop.get_info(info_name="total_price", info_id=bike_id, table_name="order_history")
                            total_price = bike_shop.get_info(info_name="total_price", info_id=choice, table_name="order_history")

                            if choice1 == "1" and order_info == "Purchase":
                                print(f"Do you want to return back to {piece_info} bikes called {name_info} ?")
                                print(f"You will be paid {price_info:,.2f} TRY in total")
                                print("Would you like to pay it now ?")
                                yes_no = input("Enter your answer( Yes/No ): ")
                                if yes_no.lower().capitalize() == "Yes":
                                    bike_shop.update_info(info_type="integer", info_name="stock", info_id=bike_id, table_name="products", new_value=(stock_info + piece_info))
                                    database.cursor.execute(f"Delete From order_history Where id = {choice}")
                                    database.con.commit()
                                    print(f"\033[1;32mYou have successfully returned your product!\033[m")
                                break

                            elif choice1 == "2" and order_info != "Purchase":
                                now = datetime.now()
                                order_time = bike_shop.get_info(info_name="order_time", info_id=choice, table_name="order_history")
                                d1 = datetime.strptime(order_time, "%d/%m/%Y %H:%M:%S")
                                delta = now- d1
                                hours = int(delta.seconds / (60*60))
                                minutes = int(delta.seconds / 60)
                                minutes_2 = minutes % 60

                                total_rent_cost = total_price * (minutes / 60)
                                total_rent_cost_yellow = f"\033[93m{total_rent_cost}\033[m"
                                print(
                                    f"{piece_info} {name_info} cost {total_rent_cost_yellow} {money.CURRENCY} for {hours} hours {minutes_2} minutes")
                                print("Would you like to pay it now ?")
                                yes_no = input("Enter your answer( Yes/No ): ")
                                 
                                if yes_no.lower().capitalize == "Yes":
                                    bill = money.payment(total_rent_cost)
                                    if bill:
                                        bike_shop.update_info(info_type="integer",info_name="stock",info_id=bike_id,table_name="products",new_value=(stock_info + piece_info))
                                        database.cursor.execute(f"Delete From order_history Where id = {choice}")
                                        database.con.commit()
                                    break
                                break
                            elif choice1 == "3":
                                print("Returning to main menu")
                                time.sleep(2)
                                break
                            else:
                                print("\033[31mInvalid value, Please try again.\033[m")
                                continue
                    except ValueError:
                        print("\033[31mInvalid value. Please enter integer number\033[m")
                        continue
    if choice ==  "Exit":
            print("\033[1;32mYou've successfully exited from the program.\033[m")
            break

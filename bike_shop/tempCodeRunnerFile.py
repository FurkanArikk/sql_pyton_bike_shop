while True:
                try:
                    print(f"Current stock is: {stock_info}")
                    how_many = int(input("How many bikes would you like to buy ?: "))

                    if how_many > stock_info:
                        print("\033[31mYou can't buy more than current stock!\033[m")
                        continue
                    if how_many == 0:
                        print("You're returning the main menu...")
                        time.sleep(2)
                    break
                except ValueError:
                    print("\033[31mYour choice must be an integer, Please write in correct type!\033[m")
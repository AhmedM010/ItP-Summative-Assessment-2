def PrintItemDetail (ChosenItem, ItemPrice, TotalMoneyGiven):
    '''
    Prints item details including selected item, price, and total money given by the user. To avoid redundancy
    '''
    print(f"You selected: {ChosenItem[0]} - {ChosenItem[1]}")
    print(f"Item Price: {ItemPrice} AED")
    print(f"You've given: {TotalMoneyGiven} AED")

def DisplayItemFunc (items): 
    '''
    Displays the items in a three neat column table after a selecting a category   
        - formats the tuples (code, name, price) to "code name, price"
        - iterates by groups of three

    The Parameters
    items - a dictionary with an str key and a list value and the list within is a list of tuples, 
    where each tuple represents an item with the structure (str1, str2, str3) 
    '''
    # Loops through the items list in steps of 3 (for grouping rows with 3 items each)
    for i in range (0, len(items), 3):
        # Creates a list of formatted strings for the current row of items
        column = [f"{items[x][0]} {items[x][1]}: {items[x][2]}" # Formats (code, name, price) to "code name: price"
            if x < len(items) # Makes sure we dont go past the list
            else "" # Prints an empty cell if there is no item
            for x in range(i,i+3)] # Processing in groups of 3 items
        
        # Sorts into 3, 30-character long, neat columns and prints
        print(f"{column[0]:<30} {column[1]:<30} {column[2]:<30}") 


def ValidateInput (prompt, GivenChoices): 
    '''
    Makes sure that the user enters ONLY valid inputs wihtin given choices.
    - It'll prompt over and over until given a valid input
    - Strips whitespace from the user's input and converts it to lowercase for consistency.
    - If the input is invalid (ie: not in the GivenChoices parameter); informs the user and prompts again.

    The Parameters:
    - prompt: A string with the message shown to the user when asking for input. ie: "Please pick a catergory to explore! (Q to quit)"
    - GivenChoices: A collection (list, tuple, set) of only valid inputs that the user is allowed to enter.

    Returns:
    - It returns the valid input given by the user, stripped of whitespace and converted into lowercase
    '''
    # While loop to continuously prompt
    while True:
        # Prompts the user for input and cleans it by removing whitespace and converting to lowercase
        UserInput = input(prompt).strip().lower()

        # Checks if the input is in the list of valid inputs
        if UserInput in GivenChoices:
            return UserInput # Exits the loop and returns the valid input
        print("Invalid input. Please try again.") # Triggers when user input isn't listed in GivenChoices


def PaymentProcess (ChosenItem, ItemPrice, CurrencyOptions, Navigation): 
    """
    Processes the payment for a selected item by continuously asking the user for valid input in CurrencyOptions.
    
    Parameters:
    - ChosenItem (tuple): The selected item (code, name, price).
    - ItemPrice (float): The price of the chosen item in AED. (split to get the numerical value for comparison to TotalMoneyGiven)
    - CurrencyOptions (list): A list of valid denominations of currency .
    
    Functions:
    - PrintItemDetail: Prints item details including selected item, price, and total money given by the user. To avoid redundancy

    Returns:
    - TotalMoneyGiven (float): The total amount of money given by the user.
    """
    # Sets TotalMoneyGiven as 0 to start
    TotalMoneyGiven = 0

    # Loop until the total money given by the user is greater than or equal to the item's price
    while TotalMoneyGiven < ItemPrice:

        # Displays the selected item details (code,name,price) and the current total money given
        PrintItemDetail (ChosenItem, ItemPrice, TotalMoneyGiven)

        # Asks the user to enter a numeric payment amount and cleans it by removing whitespace and converting to lowercase
        UserPPInput = input(f"Please enter payment {CurrencyOptions}('Back' to return, 'Q' to quit): ").strip().lower()

        # Checks if the input is a valid denomination in Currency Options
        if UserPPInput in Navigation:

            # Refunds money and goes back to item selection, if user inputs 'back'
            if UserPPInput == "back":
                print(f"\nRefunding {TotalMoneyGiven}...") # Notifies user of the amount of the refund owed 
                print(f"{TotalMoneyGiven}AED has been added to your invertory") # Notifies user that thei money has been refunded
                return None
            # Exits if user inputs 'q'
            elif UserPPInput == "q":
                print("Thank you for using our vending machine!")
                quit()
        try:
            # Converts payment process input into a numerical number
            UserMoneyInput = float(UserPPInput)

            # Checks if the user's input is a valid denomination
            if UserMoneyInput in CurrencyOptions:
                TotalMoneyGiven += UserMoneyInput # Add the valid input to the total
            else:
                # Notify the user if the entered denomination is invalid
                print("Invalid denomination. Try again.")
        except ValueError:
            # Notify user when input is a non-numeric, non-navigational value
            print("Invalid input. Please enter a valid input.")

    # Display the final payment details after the user has given enough money
    PrintItemDetail (ChosenItem, ItemPrice, TotalMoneyGiven)

    # Return the total money given
    return TotalMoneyGiven         

def PurchaseConfirmation (ChosenItem, TotalMoneyGiven, ItemPrice): 
    '''
    Handles the confirmation of a purchase after the user has paid the necessary amount.
    - Prompts the user to confirm whether they want to finalize the purchase.
    - confirmed, it displays the success message and calculates the change to be returned, if any.
    - not confirmed, it cancels the order and processes the refund to be returned.
    - quit, ends the program

    The Parameters:
    - ChosenItem (tuple): The selected item (code, name, price).
    - TotalMoneyGiven (float): The total amount of money given by the user.
    - ItemPrice (float): The price of the chosen item in AED.

    Functions:
    - ValidateInput: Ensures user inputs are valid.

    Returns:
    - None: The function prints messages confirming or cancelling the purchase.
    '''
    # Prompts the user to confirm payment and cleans it by removing whitespace and converting to lowercase
    PaymentConfirmation = ValidateInput("Confirm payment? (yes/no) (Q to quit): ", ["yes","no", "q"])

    #If user confirms payment
    if PaymentConfirmation == 'yes':
        print(f"\nPayment confirmed! {ChosenItem[1]} has been purchased.") # Notifies user the the payment has been confirmed
        UserChange = TotalMoneyGiven - ItemPrice #Change calculation process
        print(f"Your change is {(UserChange)}AED! Dispensing change..") # Notifies user of the amount of change owed
        print(f"{UserChange}AED has been added to your invertory") # Notifies user that the change has been dispensed
        print(f"\nDispensing {ChosenItem[1]}...") # Notifies user that the chosen item is being dispensed
        print(f"The snack {ChosenItem[1]} is ready for collection!") # Notifies user that the chosen item dispensed and ready for collection

    #If user cancels payment    
    elif PaymentConfirmation == 'no':
        print("\nPayment not confirmed. Cancelling the order.") # Notifies user of the purchase cancellation
        print(f"Refunding {TotalMoneyGiven}AED...") # Notifies user of the amount of the refund owed 
        print(f"{TotalMoneyGiven}AED has been added to your invertory\n") # Notifies user that thei money has been refunded

    # Exit if the user inputs 'q'
    else:
        print("Thank you for using our vending machine!")
        quit()



def vending_machine():
    '''
    Simulates a vending machine, allowing users to:
    - Explore categories and items (Snacks, Sweets, Drinks).
    - Select items from a specific category.
    - Make payments with valid denominations.
    - Confirm purchase and recieve change or cancel and receive refunds.

    Functions:
    - ValidateInput: Ensures user inputs are valid.
    - DisplayItemFunc: Displays items neatly in a 3-column layout.
    - PaymentProcess: To handle payment input and ensure correct amounts are entered.
    - PurchaseConfirmation: To handle the confirmation of purchase and the user's change or refund.

    Flow:
    1. User is welcomed and presented with available categories to choose.
    2. After selecting a category, available items, within the chosen category, are displayed.
    3. User chooses an item or navigates back to categories.
    4. Payment is processed by accepting valid denominations.
    5. The purchase is confirmed or canceled, with change given or refunded respectively.

    Dependencies:
    - `categories`: Dictionary of the categories' codes and names.
    - `items`: Dictionary of categories' codes mapped to lists of item tuples that contain the item in said category.
    - `Currency`: List of valid currency denominations.
    - `Navigation`: A list of prompts for navigating the different prompts

    Returns:
    - None. Runs indefinitely until the user chooses to quit.
    '''
    # Greets user with a welcome prompt
    print("Hey!! Welcome to the GMYM Vending Machine! The Vending Machine to all your Vending Machine needs!!")

    # Defines categories and items
    categories = {"a": "Snacks", "b": "Sweets", "c": "Drinks"}
    items = {"a": Snacks, "b": Sweets, "c": Drinks}

    # While loop to contionuously prompt about categories. (used to help navigation between prompts)
    while True:
        # Display categories
        print("Categories:")

        # Display categories for the user to select
        for key, name in categories.items():
            print(f"{key.upper()} {name}")

        # Prompts user to select a category or quit
        UserChoice = ValidateInput("Please pick a catergory to explore! (Q to quit): ", list(categories.keys()) + ["q"])

        # Exit if the user inputs 'q'
        if UserChoice == "q":
            print("Thank you for using the vending machine!")
            quit()

        # Item selection loop within the chosen category
        while True:

            # Fetch the selected category's list of items
            CategoryItems = items[UserChoice]

            # Display items in the selected category in a neat 3-columns format
            DisplayItemFunc(CategoryItems) 

            # Prompt the user to select an item, go back to categorie, or quit
            ChosenItemCode = ValidateInput("Please enter the code of your item! ('Back' to return, 'Q' to quit): ",[item[0].lower() for item in CategoryItems] + ["back", "q"])

            # Exit the current loop and return to category selection prompt if user inputs 'back'
            if ChosenItemCode == "back":
                break

            # Exit if the user inputs 'q'
            elif ChosenItemCode == "q":
                print("Thank you for using the vending machine!")
                quit()

            # Proceed to payment process if a valid item is selected
            # Looped to seperate the payment process prompt and the item selection prompt
            while True:
                # Find the chosen item from the list using its itemcode and matching it with the chosen item code earlier.
                ChosenItem = next(item for item in CategoryItems if item[0].lower() == ChosenItemCode)

                # Extracts the numerical price from the item's details for change calculation in PurchaseConfirmation function.
                ItemPrice = float(ChosenItem[2].split()[0])

                # Initiate the payment process
                TotalMoneyGiven = PaymentProcess(ChosenItem, ItemPrice, Currency, Navigation)

                # Exit the current payment process and return to item selection,if user inputs 'back'
                if TotalMoneyGiven is None:  # User inputted back in payment process
                    break  # Return to the item selection screen

                # Confirms the purchase and processes change or refund if necessary, go back to category selection, or quit
                PurchaseConfirmation(ChosenItem, TotalMoneyGiven, ItemPrice)
                
                # End the session with a thank you message
                print("Thank you for using our vending machine!")
                quit() # Exit the function and the session

#Data
    '''
    Categories Dictionary:
    The 'Categories' dictionary maps category codes (A, B, C) to their respective names.
    Each category represents a group of items that the user can select.
    Categories:
     - "A": Snacks
     - "B": Sweets
     - "C": Drinks
    '''
Categories =  {"A":"Snacks","B":"Sweets","C":"Drinks"}

# Items Lists:
'''
Each category has a corresponding list of items represented as tuples.
Each item is a tuple with three elements:
- Item code (e.g., 'A01')
- Item name (e.g., 'Lays')
- Price (e.g., '4 AED')
'''
# Snacks: List of snack items available in the vending machine.
Snacks = [('A01', 'Lays', '4 AED'),
    ('A02', 'Cheetos', '3.50 AED'),
    ('A03', 'Doritos', '3.50 AED'),
    ('A04', 'Pringles', '6 AED'),
    ('A05', 'Takis', '4 AED')]
# Sweets: List of sweet items available in the vending machine.
Sweets  = [('B01', "Hershey's Choco", '3.50 AED'),
    ('B02', "Hershey's C&C", '3.50 AED'),
    ('B03', 'KitKat', '3 AED'),
    ('B04', 'Snickers', '3 AED'),
    ('B05', 'Mars', '3 AED'),
    ('B06', 'Twix', '3 AED'),
    ('B07', 'Galaxy Milk Choco', '3.50 AED'),
    ('B08', 'Galaxy Caramel', '3.50 AED'),
    ('B09', 'Toblerone Mini', '5 AED'),
    ('B10', 'Ferrero Rocher (3 pcs)', '7 AED')]
# Drinks: List of drink items available in the vending machine.
Drinks  = [('C01', 'Regular Coke', '2.50 AED'),
    ('C02', 'Coke Zero', '2.50 AED'),
    ('C03', 'Sprite', '2.50 AED'),
    ('C04', 'Pepsi', '2.50 AED'),
    ('C05', 'Fanta', '2.50 AED'),
    ('C06', 'Mountain Dew', '2.50 AED'),
    ('C07', 'Coke Bottle (500ml)', '3.50 AED'),
    ('C08', 'Pepsi Bottle (500ml)', '3.50 AED'),
    ('C09', 'Mtn Dew Bottle (500ml)', '3.50 AED'),
    ('C10', 'Monster Energy', '8 AED'),
    ('C11', 'Lipton Peach Iced Tea', '3.50 AED'),
    ('C12', 'Gatorade Blue', '4 AED'),
    ('C13', 'Strawberry Milk', '3 AED'),
    ('C14', 'Choco Milk', '3 AED'),
    ('C15', 'Water (500ml)', '1 AED')]

# Currency Denominations List:
'''
'Currency' contains valid denominations that users can input to pay the vending machine.
The valid denominations are:
- 0.5 AED (50 fils)
- 1 AED
- 5 AED
- 10 AED
- 20 AED
'''
Currency = [0.5,1,5,10,20]

# Navigation Options List:
'''
'Navigation' contains two options available for the user to navigate through the vending machine prompts.
- "back": Option to go back to the previous menu (e.g., category selection or item selection).
- "q": Option to quit the vending machine at any time.
'''
Navigation = ["back","q"]

vending_machine()
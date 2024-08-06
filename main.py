import random
current_category = "Fruits"
category_array = ("Fruits","Vegetables","Cars","Anime")
# fruits = ("Apple","Orange")
# Vegetables = ("Apple","Orange")
# cars = ("Apple","Orange")
# category_dict = {"fruits":["Apple","Orange","Banana",""]}

def ask_user_input():
    user_input = ''
    exit_condition = False
    
    while exit_condition == False:
        if type(user_input) == int:
            exit_condition = True
            break

        try:
            user_input = int(input("Enter your choice: "))            
            break

        except:
            print("Please only enter integers.")
        
    return user_input

def get_category():
    global current_category
    print("-------------------------------------------------------")
    print("""Category page
0. Exit""")
    id = 0
    for category in category_array:
        id+=1
        print("{}. {}".format(id,category_array[id-1]))
    
    category_user_input = ask_user_input()
    
    if category_user_input == 0:
        main()
        return 0
    
    for i in range(len(category_array)):

        if category_user_input == i+1:
            current_category = category_array[i]
            print("Category is updated to",current_category)
            break

    if category_user_input > len(category_array):
        print("Not in the limit. Please reselect")
    
    main()
    
    
def start_game():
    #The game starts here
    print("Hello World")

def main():
    print()
    print("-------------------------------------------------------")
    print("Hangman Game Simple")
    print("-------------------------------------------------------")
    print("""
    Current Category Selection: {}
    0. Exit
    1. Select Categories
    2. Start Game
    """.format(current_category))
    
    main_user_input = ask_user_input()
    if main_user_input == 0:
        # Peacefully exit the system
        exit(1)
    elif main_user_input == 1:
        get_category()
        print("-------------------------------------------------------")
    elif main_user_input == 2:
        start_game()
    else:
        print("Not a valid input")
        main()

if __name__ == '__main__':
    main()
    print("-------------------------------------------------------")
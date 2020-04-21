from pyswip import Prolog
import easygui

prolog = Prolog()
prolog.consult("mysubway.pl")
order_count = 0

def main():
    ordering()

def order_counter():
    global order_count
    order_count = order_count + 1

def ask_wanted(item_title, max_items, append_msg):
    return easygui.choicebox(msg="{}\nAre you ready to proceed with choosing your {}?\nYou can choose maximum {} item(s)\nPress 'next' if you dont want to choose '{}' and proceed to next item"
                             .format(append_msg, item_title, max_items, item_title), choices=['yes', 'next'],
                             title="Subway Order")

# def ask_choice(item_title, item, choices_left):
#     return easygui.choicebox(msg="Please chose your {}\nYou have {} choices left\nDo you want {}?\nPress 'next' to choose other item"
#                              .format(item_title, choices_left, item),
#                              choices=['yes', 'no', 'next'], title="Subway Order")


#displays menu choices
def ask_choice(item_title, item_list, choices_left, append_msg):
    choice_list = []
    for el in item_list:
        choice_list.append(el['X'])
    choice_list.append('next')
    return easygui.choicebox(msg="{}\nPlease chose your {}\nYou have {} choices left\nPress 'next' to choose other item"
                             .format(append_msg, item_title, choices_left),
                             choices=choice_list, title="Subway Order")

def find_and_remove(item_list, target):
    for el in item_list:
        if el['X'] == target:
            item_list.remove(el)
    return item_list

#select a product type
def select_item(item_title, item_list, max_items, choice_required):
    choices_made = 0

    response = ask_choice(item_title, item_list, max_items - choices_made, "")
    if(choice_required):
        while (response == "next"):
            response = ask_choice(item_title, item_list, max_items - choices_made, "YOU MUST CHOOSE AT LEAST ONE {}".format(item_title))
    prolog.assertz("{}_chosen({})".format(item_title, response))
    item_list = find_and_remove(item_list, response)
    # print("pajibat Response = ", response)
    choices_made = choices_made + 1

    # if user selects item, keep asking for more
    while(choices_made != max_items and response != "next" and item_list):
        response = ask_choice(item_title, item_list, max_items - choices_made, "")
        if response == "next":
            break
        prolog.assertz("{}_chosen({})".format(item_title, response))
        item_list = find_and_remove(item_list, response)
        choices_made = choices_made + 1

    for el in item_list:
        if el['X'] == response:
            item_list.remove(el)

    # chosen_list = list(prolog.query("{}_chosen(X)".format(item_title)))
    # for el in range(len(chosen_list)):
    #     print(chosen_list[el]['X'])

def order_item(item_title, max_count, choice_required):
    item_list = list(prolog.query("{}_choice(X)".format(item_title)))
    # print(item_list)

    # initially set chosen as null
    prolog.assertz("{}_chosen(null)".format(item_title))
    if item_list == []:
        order_counter()
        return

    if max_count == -1:
        max_count = len(item_list)

    while True:
        response = ask_wanted(item_title, max_count, "" if not choice_required else "CHOICE REQUIRED")
        if(response == "yes" or not choice_required):
            break

    if (response == 'yes'):
        select_item(item_title, item_list, max_count, choice_required)
        order_counter()
    elif (response == "next"):
        order_counter()
    # else:
    #     return easygui.textbox("Good bye, see you next time")

#ordering sequence
def ordering():
    reply = easygui.choicebox(msg="Would you like to start ordering?", choices=['yes','no'], title="Subway Order")
    print(reply)

    if(order_count == 0):
        if(reply == 'yes'):
            order_counter()
        else:
            return easygui.textbox("Good bye, see you next time")

    if(order_count == 1):
        order_item("meal", 1, True)
    if(order_count == 2):
        order_item("bread", 1, True)
    if(order_count == 3):
        order_item("meat", 1, False)
    if(order_count == 4):
        order_item("veggie", -1, False)
    if(order_count == 5):
        order_item("cheese", 1, False)
    if(order_count == 6):
        order_item("sauce", -1, False)
    if(order_count == 7):
        order_item("addons", -1, False)

    # print all choices
    if(order_count == 8):
        print("\---  YOUR ORDER  ---/")
        print_choices(prepare_choice_list("meal"), "Meal")
        print_choices(prepare_choice_list("bread"), "Bread")
        print_choices(prepare_choice_list("meat"), "Meat")
        print_choices(prepare_choice_list("veggie"), "Veggie")
        print_choices(prepare_choice_list("cheese"), "Cheese")
        print_choices(prepare_choice_list("sauce"), "Sauce")
        print_choices(prepare_choice_list("addons"), "Addons")

def prepare_choice_list(item_name):
    choice_list = list(prolog.query("{}_chosen(X)".format(item_name)))
    return choice_list[1:] if len(choice_list) > 1 else choice_list

def print_choices(product_list, product_name):
    print(product_name, "choice:", end = " ")
    # print("Array size = ", len(product_list))
    for el in product_list:
        if(el['X'] == "null"):
            print("NA", end = " ")
        else:
            print(el['X'], end = " ")
    print()

# Run the main program
if __name__ == "__main__":
	main()

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

def ask_wanted(item_title, max_items):
    return easygui.choicebox(msg="Are you ready to proceed with choosing your {}?\nYou can choose maximum {} item(s)\nPress 'next' if you dont want to choose '{}' and proceed to next item"
                             .format(item_title, max_items, item_title), choices=['yes', 'next'],
                             title="Subway Order")

# def ask_choice(item_title, item, choices_left):
#     return easygui.choicebox(msg="Please chose your {}\nYou have {} choices left\nDo you want {}?\nPress 'next' to choose other item"
#                              .format(item_title, choices_left, item),
#                              choices=['yes', 'no', 'next'], title="Subway Order")

def ask_choice(item_title, item_list, choices_left):
    choice_list = []
    for el in range(len(item_list)):
        choice_list.append(item_list[el]['X'])
    choice_list.append('next')
    return easygui.choicebox(msg="Please chose your {}\nYou have {} choices left\nPress 'next' to choose other item"
                             .format(item_title, choices_left),
                             choices=choice_list, title="Subway Order")


def select_item(item_title, max_items):
    item_list = list(prolog.query("{}_choice(X)".format(item_title)))
    choices_made = 0
    for el in range(len(item_list)):
        current_item = item_list[el]['X']
        response = ask_choice(item_title, item_list, max_items - choices_made)
        if(response == "next"):
            break
        elif(response == "yes"):
            prolog.assertz("{}_chosen({})".format(item_title, current_item))
            choices_made = choices_made + 1
            #if max choice limit has been reached
            if(choices_made == max_items):
                break

    chosen_list = list(prolog.query("{}_chosen(X)".format(item_title)))
    for el in range(len(chosen_list)):
        print(chosen_list[el]['X'])

def order_item(item_title, max_count):
    response = ask_wanted(item_title, max_count)

    # initially set chosen as null
    prolog.assertz("{}_chosen(null)".format(item_title))
    if (response == 'yes'):
        select_item(item_title, max_count)
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
        order_item("meal", 1)
    if(order_count == 2):
        order_item("bread", 1)
    if(order_count == 3):
        order_item("meat", 1)
    if(order_count == 4):
        order_item("veggie", 5)
    if(order_count == 5):
        order_item("cheese", 1)
    if(order_count == 6):
        order_item("sauce", 3)
    if(order_count == 7):
        order_item("addons", 3)
    # print all choices
    if(order_count == 7):
        veggies = list(prolog.query("veggie_chosen(X)"))[0]['X']
        print(list(prolog.query("bread_chosen(X)"))[0]['X'],
              list(prolog.query("meat_chosen(X)"))[0]['X'],
              list(prolog.query("veggie_chosen(X)"))[0]['X'],
              list(prolog.query("cheese_chosen(X)"))[0]['X'],
              list(prolog.query("sauce_chosen(X)"))[0]['X'],
              list(prolog.query("addons_chosen(X)"))[0]['X'])
        print(len(veggies) - 1) # nes pirmas yra null

    print(list(prolog.query("veggie_chosen(X)")))
def offer_choices():
    print("test")

# Run the main program
if __name__ == "__main__":
	main()

/* Adds element to a list */
append([A | B], C, [A | D]) :- append(B, C, D).
append([], A, A).

/* value meals wont offer addons; healthy will offer healthy sauces and no addons; vegetarian just no meat */
meals([standard, value, healthy, vegetarian]).
breads([multigrain, italian, flatbread, wheat, honeyoat, rye, heartyitalian, montereycheddar]).
meats([ham, bacon, teriyaki, bbqchicken, meatball, turkey]).
veggies([cucumber, greenpepper, lettuce, avocado, spinach, tomato, jalapenos, pickles, olives]).
cheese([american, monterrey, feta, mozzarella, swiss]).
sauces([chipotle, mayonaise, bbq, creamy_italian, caesar]).
healthy_sauces([oil, mustard, onion]).
addons([drink, chips, cookie]).

meal_choice(X) :-
    meals(L), member(X, L).

bread_choice(X) :-
    breads(L), member(X, L).

/* findall(Object,Goal,List). */
meat_options(X) :- findall(X, (\+meal_chosen(vegetarian), meats(X)), X). /* returns list of possible options, empty list if doesnt match criterias */
meat_list(X) :- meat_options(L), member(X, L). /*  */
meat_choice(X) :- meat_list(L), member(X, L).

veggie_choice(X) :-
    veggies(L), member(X, L).

cheese_choice(X) :-
    cheese(L), member(X, L).

sauce_options(X) :- findall(X, (meal_chosen(healthy) -> healthy_sauces(X);
							sauces(S), healthy_sauces(H), append(S, H, X)), X).
sauce_list(X) :- sauce_options(L), member(X, L).
sauce_choice(X) :- sauce_list(L), member(X, L).


addons_options(X) :- findall(X, (\+meal_chosen(value), \+meal_chosen(healthy), addons(X)), X).
addons_list(X) :- addons_options(L), member(X, L).
addons_choice(X) :- addons_list(L), member(X, L).

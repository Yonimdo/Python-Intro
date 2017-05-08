

print("Hello World")

# Comment

'''
Multi line
Comment
'''
name = "Yoni"


print("5 ** 3 = ",5**3)

print("5 // 1 = ",5//1)

print("5 // 2 = ",5//2)

print("5 // 3 = ",5//3)

print("%s %s %s" % (name, "number", 1))

print("\n"*5)
print("I Dont Like", end="")
print(" new lines")

grocery_list = ['Juice', "Text", "Not cool"]
print(grocery_list[0])
print(grocery_list[0:3])
other_events = ["Wash car", "Have sex", 2]
to_do_list = [grocery_list,other_events]
# Union
to_do_list2 = grocery_list+other_events
print(to_do_list)
print(to_do_list2)
# Prints Have sex
print(to_do_list[1][1])
grocery_list.append("Onion")
print(to_do_list)
grocery_list.insert(1, "Onion")
print(to_do_list)
grocery_list.remove("Onion")
print(to_do_list)
del grocery_list[3]
grocery_list.insert(1, "Onion")
print(to_do_list)
grocery_list.sort()
print(to_do_list)
grocery_list.reverse()
print(to_do_list)
print(len(grocery_list), " ", len(to_do_list))
print(max(grocery_list))
print(min(grocery_list))
pi_tuple = (3, 1, 4, 1, 5, 9)
new_list = list(pi_tuple)
new_tuple = tuple(new_list)
print(max(pi_tuple))
dictionary = {"1":"one",
              "2":"two"}

print(dictionary["1"])

del dictionary["1"]

dictionary["2"] = "two changed"

print(dictionary.keys())
print(dictionary.get("2"))
print(dictionary.values())



def find_the_parent(child):
    for a_class in [Drinks, Pastry, Sweets]:
        if issubclass(child, a_class):
            print(a_class.__name__)

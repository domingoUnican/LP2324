def create_class(name, attrs):
    return type(name, (object,), attrs)


def create_class2(name, attrs):
    return type(name, (MyClass,), attrs)


# Example usage:
attrs = {
    'say_hello': lambda self: print('Hello, world!'),
    'x': 10,
}

MyClass = create_class('MyClass', attrs)
instance = MyClass()
instance.say_hello()  # prints: Hello, world!
print(instance.x)  # prints: 10

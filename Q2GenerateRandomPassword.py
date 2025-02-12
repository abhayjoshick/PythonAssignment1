import random
import string

def generate_password():
    all_chars = string.ascii_letters + string.digits + "!@#$%&*"

    passwd = set()
    
    passwd.add(random.choice(string.ascii_uppercase))  
    passwd.add(random.choice(string.ascii_lowercase))  
    passwd.update(random.sample(string.digits, 2))      
    passwd.add(random.choice("!@#$%&*"))            

    while len(passwd) < 16:
        passwd.add(random.choice(all_chars))

    passwdList = list(passwd)

    random.shuffle(passwdList)

    return "".join(passwdList)

print("Generated Password:", generate_password())

print(generate_password())

print(generate_password())
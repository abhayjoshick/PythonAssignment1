def validatEmail(email: str) -> str:
    if not email.endswith("@gmail.com"):
        return "Invalid Gmail address."
    
    username = email[:-10]  

    if len(username) == 0:
        return "Invalid Gmail address: Username cannot be empty."
    
    allowed = set("abcdefghijklmnopqrstuvwxyz0123456789._-")
    
    if any(ch not in allowed for ch in username):
        return "Invalid Gmail address: Username contains invalid chacters."
    
    return "Valid Gmail address"
email = input("Enter email to validate: ")
print(validatEmail(email))
def validIp(ip: str) -> str:
    octets = ip.split(".")
    if len(octets) != 4:
        return "Invalid IPv4 address"
    
    for octet in octets:
        if not octet.isdigit() or not (0 <= int(octet) <= 255):
            return "Invalid IPv4 address: Each octet must be a number between 0 and 255."
    
    first = int(octets[0])
    second  = int(octets[1])
    
    if first == 10 or (first == 192 and second == 168) or (first == 172 and 16 <= second <= 31):
        return "Private IPv4 address"
    
    return "Public IPv4 address"

ip = input("Enter IP to validate: ").strip() 
print(validIp(ip))  

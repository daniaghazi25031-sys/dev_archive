def encryption(text,shift):
    result=""
    for char in text:
       if char.islower:
          char_upper=char.upper()
          s=chr((ord(char_upper)+shift-65)%26+65)
          result+=s.lower()
       
       #else:
            #result+=char
    return result
    

print(encryption("#$",8))

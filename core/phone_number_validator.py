def validate_phone_number(phone_number):
    if phone_number[0] == "+":
        return phone_number
    elif phone_number[0] != "+":
        return f"+{phone_number}"

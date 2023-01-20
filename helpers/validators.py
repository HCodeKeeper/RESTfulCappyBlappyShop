def validate_phone_number(number):
    MIN_LENGTH = 9
    MAX_LENGTH = 13
    if len(number) in range(MIN_LENGTH, MAX_LENGTH):
        try:
            int(number)
        except Exception:
            pass
        else:
            if phone_number_exist(number):
                return True
    return False


def phone_number_exist(number):
    return True
    pass

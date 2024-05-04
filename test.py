from datetime import datetime

def convertCurentTimeToNumber():
    current_datetime = datetime.now()
    datetime_in_decimal = float(current_datetime.timestamp())  
    return datetime_in_decimal


def convertDecimalToDateTime(decimal_timestamp):
    # Convert the decimal timestamp to a datetime object
    datetime_obj = datetime.fromtimestamp(decimal_timestamp)
    # Format the datetime object as "YYYY-MM-DD HH:MM:SS"
    formatted_datetime = datetime_obj.strftime("%Y-%m-%d %H:%M:%S")
    return formatted_datetime

valTime = convertCurentTimeToNumber()
print(valTime)
valStr = convertDecimalToDateTime(valTime)
print(valStr)
def transform_to_json_send(data_json):
    json_send = {
        "status": True,
        "status_code": 200,
        "message": "Success",
        "data": data_json
    }
    return json_send

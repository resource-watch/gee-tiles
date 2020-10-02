from flask import jsonify


# GENERIC Error


def error(status=500, detail='Generic Error'):
    error = {
        'status': status,
        'detail': detail
    }
    return jsonify(errors=[error]), status

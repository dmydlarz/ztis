from random import randint

def getData():
	return """
{
    "events": [{
        "name": "event """ + str(randint(0, 999999)) + """",
        "type": "type 1",
        "frequency": 1,
        "deviation": 0.05,
        "correlation": [{
            "id": 1,
            "after": 0.5,
            "deviation": 0.1
        }]
    }, {
        "name": "event """ + str(randint(0, 999999)) + """",
        "type": "type 1",
        "correlation": [{
            "id": 2,
            "after": 0.5,
            "deviation": 0.1
        }, {
            "id": 3,
            "after": 0.2,
            "deviation": 0.08
        }]
    }, {
        "name": "event """ + str(randint(0, 999999)) + """",
        "type": "type 2",
        "correlation": [{
            "id": 3,
            "after": 1,
            "deviation": 0.01
        }]
    }, {
        "name": "event """ + str(randint(0, 999999)) + """",
        "type": "type 2"
    }]
}
		"""
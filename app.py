from flask import Flask, request, jsonify
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

app = Flask(__name__)


@app.route('/turn-on', methods=['POST', 'GET'])
def turn_on():
    if request.method == 'POST':
        status = request.json.get('status', None)
        led_number = request.json.get('led_number', None)
        if led_number:
            led_number = int(led_number)
            GPIO.setup(led_number, GPIO.OUT)
            print(led_number)
        print(status)
        if status == 'on':
            manipulate_pin(led_number, 1)
        elif status == 'off':
            GPIO.output(led_number, 0)
        return jsonify(status=status)
    elif request.method == 'GET':
        response = {'status': 'The led is off'}
        led_number = request.json.get('led_number', None)
        if led_number:
            led_number = int(led_number)
            status = get_pin_status(led_number)
        print(status)
        if status == 1:
            response.update({'status': 'The led is on'})
        return jsonify(response)

@app.route('/lamp', methods=['POST', 'GET'])
def lamp():
    if request.method == 'POST':
        status = request.json.get('status', None)
        GPIO.setup(21, GPIO.OUT)
        GPIO.output(21, 1)
        if status == 'on':
            print(status)
            GPIO.output(21, 0)
        return jsonify({"status": status})


def get_pin_status(led_number: int):
    GPIO.setup(led_number, GPIO.OUT)
    status = GPIO.input(int(led_number))
    return status
    
    
def manipulate_pin(led_number: int, state: int):
    if state == 1:
        GPIO.output(led_number, GPIO.HIGH)
    elif state == 0:
        GPIO.ouput(led_number, GPIO.LOW)
    
    return GPIO.input(led_number)
    

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0')
    except KeyboardInterrupt:
        GPIO.cleanup()

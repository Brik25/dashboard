from flask import Flask
from flask_restful import marshal_with, fields, Resource, Api
from time import sleep
from pyA20.gpio import gpio
from pyA20.gpio import port
from pyA20.gpio import connector


app_serv = Flask(__name__)
api = Api(app_serv)

status = {
    'pump': 0,
    'heater1': 0,
    'klap': 0,
    'valve': 0
}

# led = port.PG6
led1 = connector.gpio1p38
led2 = connector.gpio1p37
led3 = connector.gpio1p36
led4 = connector.gpio1p35
led5 = connector.gpio1p33
led6 = connector.gpio1p32

button = connector.gpio1p40

gpio.init()
gpio.setcfg(led1, gpio.OUTPUT)
gpio.setcfg(led2, gpio.OUTPUT)
gpio.setcfg(led3, gpio.OUTPUT)
gpio.setcfg(led4, gpio.OUTPUT)
gpio.setcfg(led5, gpio.OUTPUT)
gpio.setcfg(led6, gpio.OUTPUT)


class Switch_pump(Resource):
    @marshal_with({
        'status': fields.Integer(default=0)
    })
    def get(self):
        global status
        pump = status['pump'] ^ 1
        gpio.output(led2, 1)
        status['pump'] = pump
        return {'status': status['pump']}


api.add_resource(Switch_pump, '/switch-pump')


class Switch_heater1(Resource):
    @marshal_with({
        'status': fields.Integer(default=0)
    })
    def get(self):
        global status
        heater1 = status['heater1'] ^ 1
        gpio.output(led1, 1)
        status['heater1'] = heater1
        return {'status': status['heater1']}


api.add_resource(Switch_heater1, '/switch-heater1')


class Switch_klap(Resource):
    @marshal_with({
        'status': fields.Integer(default=0)
    })
    def get(self):
        global status
        heater1 = status['klap'] ^ 1
        gpio.output(led3, 1)
        status['klap'] = heater1
        return {'status': status['klap']}


api.add_resource(Switch_klap, '/switch-klap')


class Switch_valve(Resource):
    @marshal_with({
        'status': fields.Integer(default=0)
    })
    def get(self):
        global status
        heater1 = status['valve'] ^ 1
        gpio.output(led4, 1)
        status['valve'] = heater1
        return {'status': status['valve']}


api.add_resource(Switch_valve, '/switch-valve')


@app_serv.route('/start')
def start():
    return 'Старт'


@app_serv.route('/stop')
def stop():
    return 'Стоп'


if __name__ == '__main__':
    app_serv.run(debug=True, port=5001)

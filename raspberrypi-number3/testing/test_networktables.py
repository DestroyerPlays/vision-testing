from networktables import NetworkTables

NetworkTables.initialize(server='127.0.0.1')

sd = NetworkTables.getTable("SmartDashboard")

while True:
    diff_x = sd.getNumber('error_x', float('nan'))
    diff_y = sd.getNumber('error_y', float('nan'))

    print('{}, {}'.format(diff_x, diff_y))
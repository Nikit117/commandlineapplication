import argparse

devices = {}
connections = {}

def add_device(device_name, device_type, strength=5):
    if device_type not in ['computer', 'repeater']:
        print("Invalid device type")
        return
    if strength < 0:
        print("Strength cannot be negative")
        return
    if device_type == 'repeater':
        devices[device_name] = (device_type, None)
    else:
        devices[device_name] = (device_type, strength)

def add_connection(device1, device2):
    if device1 not in devices or device2 not in devices:
        print("Both devices must be added to the network first")
        return
    connections[device1].append(device2)
    connections[device2].append(device1)

def find_path(device1, device2, path=[], strength=None):
    path = path + [device1]
    if device1 == device2:
        return path
    if device1 not in connections:
        return None
    if strength is None:
        strength = devices[device1][1]
    if strength < 1:
        return None
    for device in connections[device1]:
        if device not in path:
            if devices[device][0] == 'repeater':
                new_strength = strength * 2
                new_path = find_path(device, device2, path, new_strength)
                if new_path:
                    return new_path
            else:
                new_strength = strength - 1
                new_path = find_path(device, device2, path, new_strength)
                if new_path:
                    return new_path
    return None

def print_route(device1, device2):
    path = find_path(device1, device2)
    if path:
        print("Route from " + device1 + " to " + device2 + ": " + ' -> '.join(path))
    else:
        print("No route found from " + device1 + " to " + device2)

parser = argparse.ArgumentParser(description='Network Manager')

parser.add_argument('--add_device', nargs=2, metavar=('device_name', 'device_type'), help='Add a device to the network')
parser.add_argument('--add_strength', nargs=2, metavar=('device_name', 'strength'), help='Add strength to a device')
parser.add_argument('--add_connection', nargs=2, metavar=('device1', 'device2'), help='Add a connection between two devices')
parser.add_argument('--print_route', nargs=2, metavar=('device1', 'device2'), help='Print the route between two devices')

args = parser.parse_args()

if args.add_device:
    if len(args.add_device) == 2:
        add_device(args.add_device[0], args.add_device[1])
    else:
        print("Device name and type must be provided")

if args.add_strength:
    device_name = args.add_strength[0]
    if device_name not in devices:
        raise ValueError("Device not found")
    if 'type' in devices[device_name] and devices[device_name]['type'] == 'repeater':
        raise ValueError("Strength cannot be defined for repeater")
    add_device(device_name, devices[device_name]['type'], int(args.add_strength[1]))

if args.add_connection:
    if len(args.add_connection) == 2:
        add_connection(args.add_connection[0], args.add_connection[1])
    else:
        print("Device names must be provided")

if args.print_route:
    if len(args.print_route) == 2:
        print_route(args.print_route[0], args.print_route[1])
    else:
        print("Device names must be provided")

# Path: main.py

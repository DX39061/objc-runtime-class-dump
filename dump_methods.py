#!/usr/bin/env python3
import os
import frida
import sys

class_list = open('class_list.txt', 'r').read().split('\n')
class_index = int(open('class_index.txt', 'r').read())

def parse_args():
    app_bundle_id = None
    module_name = None
    if "--app" not in sys.argv or "--module" not in sys.argv:
        sys.stderr.write("Usage: %s --app <app_bundle_id> --module <module_name>" % sys.argv[0])
        sys.exit(1)
    else:
        sys.stderr.write(" ".join(sys.argv) + "\n")
    for i in range(1, len(sys.argv)):
        if sys.argv[i] == "--app":
            app_bundle_id = sys.argv[i+1]
        elif sys.argv[i] == "--module":
            module_name = sys.argv[i+1]
    return app_bundle_id, module_name

def on_message(message, data):
    global class_index
    global session
    if message['type'] == 'send':
        if message['payload']['type'] == 'done':
            class_index += 500
            session.detach()
            if class_index >= len(class_list):
                print("all done", file=sys.stderr)
            open('class_index.txt', 'w').write(str(class_index))
            print("dump class_index " + str(class_index), file=sys.stderr)
    else:
        print(message, file=sys.stderr)

def main(bundle_id, module_name):
    global class_index
    global session
    script_path = os.path.realpath(__file__).replace('dump_methods.py', 'dump_methods.js')
    jscode = open(script_path, 'r').read()
    device = frida.get_usb_device()
    pid = device.spawn([bundle_id])
    device.resume(pid)
    session = device.attach(pid)
    script = session.create_script(jscode)
    script.on('message', on_message)
    script.load()
    class_start = class_index
    class_end = class_index + 500
    if class_end > len(class_list):
        class_end = len(class_list)
    # print("class_start: " + str(class_start) + " class_end: " + str(class_end))
    script.post({'type': 'class_list', 'module': module_name, 'data': class_list[class_start:class_end]})
    input()

if __name__ == '__main__':
    bundle_id, module_name = parse_args()
    main(bundle_id, module_name)

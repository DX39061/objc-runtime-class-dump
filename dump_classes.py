#!/usr/bin/env python3
import os
import frida
import sys

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

def main(bundle_id, module_name):
    script_path = os.path.realpath(__file__).replace('dump_classes.py', 'dump_classes.js')
    jscode = open(script_path, 'r').read()
    device = frida.get_usb_device()
    pid = device.spawn([bundle_id])
    device.resume(pid)
    session = device.attach(pid)
    script = session.create_script(jscode)
    script.load()
    input()

if __name__ == '__main__':
    bundle_id, module_name = parse_args()
    main(bundle_id, module_name)

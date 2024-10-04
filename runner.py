#!/usr/bin/env python3
import subprocess
import time
import frida
import sys
import os

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
    device = frida.get_usb_device()
    while True:    
        try:
            device.get_process(bundle_id)
            device.kill(bundle_id)
            # print("App is running")
            time.sleep(1)
        except frida.ProcessNotFoundError:
            print("next 500...")
            p = subprocess.Popen(["./dump_methods.py", "--app", bundle_id, "--module", module_name], stdout=open("method_list.txt", "a"), stderr=subprocess.PIPE)
            
            while True:
                line = p.stderr.readline()
                print(line.decode())
                if b"all done" in line:
                    exit(0)
                if b"dump class_index" in line:
                    p.terminate()
                    break

def dump_classes(bundle_id):
    p = subprocess.Popen(["./dump_classes.py", "--app", bundle_id, "--module", module_name], stdout=open("class_list.txt", "w"), stderr=subprocess.PIPE)
    while True:
        line = p.stderr.readline()
        print(line.decode())
        if b"all classes dumped" in line:
            p.terminate()
            break
        
if __name__ == '__main__':
    try:
        bundle_id, module_name = parse_args()
        dump_classes(bundle_id)
        if not os.path.exists('class_index.txt'):
            open('class_index.txt', 'w').write('0')
        main(bundle_id, module_name)
    except KeyboardInterrupt:
        exit(0)

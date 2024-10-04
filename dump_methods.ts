// console.log("Script loaded successfully ");

function dump_methods(module_base: NativePointer, classes: string[]) {
    // console.log(classes);
    for (let cls of classes) {
        if (cls == "") {
            continue;
        }
        let methods: string[] = ObjC.classes[cls].$ownMethods ;
        for (let i = 0; i < methods.length; i++) {
            try {
                let method = methods[i];
                let func = ObjC.classes[cls][method];
                let func_offset = func.implementation.sub(module_base);
                console.log(func_offset + "  " + method[0] + "[" + cls + method.slice(1) + "]");
            } catch (error) {
                // console.log(error);
            }
        }
    }
    send({
        "type": "done"
    });
}

function main() {
    recv("class_list" , (data) => {
        // console.log(data.data);
        try{
            let classes: string[] = data.data as string[];
            let module_name: string = data.module;
            let module_base: NativePointer = Module.findBaseAddress(module_name)!;
            dump_methods(module_base, classes);
        } catch (error) {
            // console.log(error);
        }
    });
}

main();
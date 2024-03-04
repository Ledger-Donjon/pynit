# PyNIT

A simple Python module for using the NIT camera library to retrieve camera image.

## Installations notes (Linux)

### Library installation

Install the NIT SDK from the NIT website.

### NUC and BPR files

Those files must be present in the 

### User permissions

The NIT Library connects to the camera by using the `/dev/ttyUSBx` device. To have the permission to read them, you have to be in the `dialout` group. To check, run the `id` command in a Terminal, and check if `20(dialout)` is present in the `groups` list.

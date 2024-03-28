Installing required Python modules in Blender
---------------------------------------------

In Blender console type:

```
import sys
sys.exec_prefix
```

It should output the path to the Python executable.

Then on the system's command line type:

```
[path/to/python]/bin/python3.[x] -m ensurepip
```

To install PIP, where [path/to/python] is the path to Blenders Python folder and [x] is the (possible) version of the Python executable.

Now the PIP executable should be installed (on Linux in the bin folder, on Windoze in the Scripts folder), and you can use it to install custom packages for example:

```
[path/to/python]/bin/pip3 install flask
```



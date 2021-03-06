# Intro

This is a brief user guide to for running distributed computing jobs on
the OSDC Griffin cluster.  We're using the [ipyparallel package](https://ipyparallel.readthedocs.org/en/latest/intro.html)
as a simple means of coordinating multiple VMs (instances in the Griffin cluster).
This project contains scripts that should make the process of setting up the cluster fairly easy.

The cluster consists of:

* The controller which manages communication between the client and engines
* 1 or more engines (which do the actual work)
* A client python script (or jupyter console) that submits python methods to be run across the cluster.

The engine connects to the controller via a ipycontroller-engine.json file that we will share using
the object store.

# Start the controller

From the Griffin console, select the latest snapshot image (`snapshot<n>`) and launch an instance.
This will be the controller instance.  Ssh into this instance and run the command

    ipcontroller [--profile <profile_name>] --ip=*

The profile name will be used to identify this
cluster within the OSDC machine.  If profile name is not provided, "profile_default" will be used.
Note: currently only the default profile is working with the engine script.

If launching more than 20 engines, run this command with 20 at a time.  Wait for the engines to activate and 
then repeat until the desired number of engines are launched.

The `ipcontroller` script will output status messages as engines and clients connect to the controller.

In a new terminal window, run the script

    /home/ubuntu/datacontainer/util/ipcontroller.sh [--profile <profile_name>]

which will copy the ipycontroller-engine.json file to the object store.

# Start the engines

From the Griffin gateway, run the script

    run_engine.sh [-c <number_of_engines>]

Number of engines specifies how many instances you wish to start.  The script will launch the indicated number of VMs.  As each VM becomes active it will read the `ipycontroller-engine.json` from from the object store and start an ipyparallel engine which connects to the controller. Note: it should not be necessary to ssh into any of the engines.

# Run the client

Now we are ready to run client programs that will utilize the cluster.  On the *controller instance* (the
terminal window where you ran ipcontroller.sh), you can run python scripts that use the ipyparallel Client
interface, or use the ipython console for interactive investigations.
To run the console type ``jupyter console``.  In either case, your code will get a client interface via::
```bash
(py34)ubuntu@ipcontroller:~$ python
Python 3.4.3 |Continuum Analytics, Inc.| (default, Oct 19 2015, 21:52:17) 
[GCC 4.4.7 20120313 (Red Hat 4.4.7-1)] on linux
Type "help", "copyright", "credits" or "license" for more information.
```
```python
>>> from ipyparallel import Client
>>> rc = Client()
>>> rc.ids
[0, 1, 2, 3]
```

The number of engine ids displayed should correspond to the the `number_of_engines` parameter used in the
`run_engine` script  (it may take a few minutes for the VMs to activate and connect to the controller).

Refer to https://ipyparallel.readthedocs.org/en/latest/multiengine.html for information on how to do
parallel operations using the Client interface.

# Shutdown the cluster

Ssh to griffin.opensciencedatacloud.org. Then, issue the following command:
```
$nova delete $(nova list | cut -d " " -f 4 | grep ipengine | tr '\n' ' ')
```

If you still see some instances that have name 'ipengine-' running, 
visit the [Griffin console](https://www.opensciencedatacloud.org/project/instances/) page,
select the engine instances,
and click "Terminate Instances".
On the controller instance (*ipcontroller*) terminal, kill the `ipcontroller` command by pressing 'Ctrl-C'.  Store any output from the controller instance into the object store. Then terminate the controller instance.

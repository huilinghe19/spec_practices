# spec_practices

   Spec can not be opened after version update(from debian to buster)on 06.08.2020, because the package libomniORB4.so.1 does not exist in this version. It exists only in debian strech version.
   
      >>> ssh -X specadm@localhost(root password)
      >>> /usr/local/spec/bin/spec
      """error while loading shared libraries: libomniORB4.so.1: cannot open shared object file: No such file or directory"""





## spec with SmarAct MCS2 controller

===== Start MCS2 Tango Device Server =====

1. Start SmarActMCS2Ctrl TangoDS 
   cd   ~/tango/DeviceClasses/Motion/MotorControllers/Smaract/SmarActMCS2Ctrl/tags/Release_1_1
   ./bin/SmarActMCS2Ctrl  testctrl
(testctrl is an instance name. The instance name must be the same in jive)
   
2. Start SmarActMCS2Motor TangoDS 
   cd  ~/tango/DeviceClasses/Motion/MotorControllers/Smaract/SmarActMCS2Motor/trunk
   ./bin/SmarActMCS2Motor testmotor
(testmotor is an instance name. The instance name must be the same in jive)

3. Open jive and check if the SmarActMCS2Ctrl and SmarActMCS2Motor TangoDS work well.

4. Setting in the SmarActMCS2Motor TangoDS. In the property, the axis number for the 3 devices(testmotor/mcs2motor/0, testmotor/mcs2motor/1, testmotor/mcs2motor/2) are: 0, 1, 2, which stands for the x,y,z direction motor of the test system. At the same time, they correspond to the channel 0, 1, 2 in telnet. 

In the attribute, Acceleration can be set as 0, Conversion can be set as 1000000000, MoveMode can be set as 0(absoulte, closed loop), SensorMode can be set as 1, SensorType can be set as 345. Speed can be set as 1000000000. The actual range of the position is from -6mm to 6mm. UnitLimitMax and UnitLimitMin can be used to set the position limits. UnitLimitMin can be set such as -5mm. UnitLimitMax can be set such as 5mm. Init and Home method should work. Calibrate can be used to calibrate the hardware at the beginning just once, when the hardware is changed, then calibrate is needed.

For the test system, the sensor types of the 3 motors are 345. When the SmarAct MCS2 motors are changed in the future, then the SensorType in TangoDS must be changed such as 348 or 349. 

5. Documentation of SmarActMCS2Ctrl TangoDS:
http://svn.code.sf.net/p/tango-ds/code/DeviceClasses/Motion/MotorControllers/Smaract/SmarActMCS2Ctrl/tags/Release_1_1/doc_html/index.html

Documentation of SmarActMCS2Motor TangoDS:
http://svn.code.sf.net/p/tango-ds/code/DeviceClasses/Motion/MotorControllers/Smaract/SmarActMCS2Motor/tags/Release_1_1/doc_html/index.html

==== Add SmarActMCS2Ctrl TangoDS in jive  ====


1. Make sure the SmarActMCS2Ctrl TangoDS is already running at first.

2. Open jive, jive >> Tools >> Server Wizard >> Server Registration >> Server name: SmarActMCS2Ctrl, Instance name: testctrl >> Start the server >> Class Selection >> Declare device >> Device Name: testctrl/mcs2ctrl/1 >> Hostname :192.168.1.200 >> PortNummer: 55551 >>ConnectType: net >>USBID (not used, pass) >>PicoScaleHostName (not used, pass) >>PicoScaleUSBID (not used, pass) >> PicoScaleConnectType  (not used, pass) >> Configuration Done.

==== Add SmarActMCS2Motor TangoDS in jive  ====


1. Make sure the SmarActMCS2Motor TangoDS is already running at first.

2. Open jive. jive >> Tools >> Server Wizard >> Server Registration >> Server name: SmarActMCS2Motor, Instance name: testmotor >> Start the server >> Class Selection >> Declare device >> Device Name: testmotor/mcs2motor/1 >>SmarActMCS2CtrlDevice: testctrl/mcs2ctrl/1  >> AxisNummer: 0 >> PicoScaleEncoded: false  >> Configuration Done.




==== Remote control from telnet  ====



1. Connect the controller using the command “telnet 192.168.1.200 55551”

2. Send the commands such as “:DEV:SNUM?”, to get the serial number of the device. The commands should be all lowercase or all uppercase.

3. Channel 0 – 2 work. In telnet, the channel 0-2 stands for the actual motor in x, y, z direction in Cartesian coordinate system. Channel 0 stands for the motor in x direction(the forward direction is positive). Channel 1 stands for the motor in y direction (the leftward direction is positive). Channel 2 stands for the motor in z direction(the downward direction is positive). This is a manually set coordinate system based on the current placement environment. In general, the actual motor corresponding to the specific channel can be known in the test session with different channel commands. 

4. Get the properties of the channels.

 To get state of channel 0: “:CHAN0:STAT?”. 

 To get position of channel 0: ":CHAN0:POS?". 

 To get the velocity of channel 0: ":CHANO:VEL?". 

 To get the move mode of channel 0: ":CHANO:MMOD?". 

 If a property value is not defined, then there is no answer.
  
5. Set the properties of the channels

 To set the move mode of channel 0: ":CHANO:MMOD 0". 

 To set the velocity of channel 0: ":CHANO:VEL 1000000000". 

 To set the acceleration of channel 0: ":CHAN0:ACC 0". 

 To set the positioner type of channel 0:":CHAN0:PTYP 345".
  
In the initialization phase, the values of above properties should be set at first.

6. Move the motor.

  //set move mode as closed loop absolute for channel 0 
  :CHAN0:MMOD 0
  // set move velocity (pm/s)
  :CHAN0:VEL 1000000000
  //disable acceleration control 
  :CHAN0:ACC 0
  // set channel 0 positioner type as 345. In the future, the positioner type must be changed as "348" (short, horizontal shift)and "349"(long, vertical shift).
  :CHAN0:PTYP 345
  // start actual movement 
  //absolute position(in pm)
  :MOVE0 5000000000


==== Remote control from PuTTy  ====


Open putty and configure the session as mcs2_telnet, then open the session and send the mcs2 control commands to the controller. 
(Due to the putty timeout problem, this method does not work. In theory, this method is feasible.)



==== Spec Control ====

1. Open spec using command "spec". Once some attributes such as move mode or limit through telnet or TangoDS are already set, then they stay always the same before the next change.

2. In spec, there are 5 motors in 2 types. "x" and "y" are spec macro motors connected with the SmarActMCS2Motor TangoDS. "test", "test2", "test3" are spec MCS2 motors. Because of the only one socket, these 2 types can not be used at the same time. If the macro motors are chosen to control the motors, then "SmarAct MCS2(Socket)" controller on spec controller screen must be set as OFF at first. Then open the SmarActMCS2Ctrl and SmarActMCS2Motor TangoDS, SPEC in oder. If the spec MCS2 motors are chosen to control the motors, then the SmarActMCS2Ctrl TangoDS must be closed at first. "SmarAct MCS2(Socket)" controller on spec controller screen must be set as ON. During these two transitions, it may take some time. If problems occur, wait a few minutes and try again.

3. "mv x 1" or "mv x -1 y 1" can be used to move the macro motors. The macro file "smaract.mac" under "/home/localadmin/macros/" is used. (https://github.com/huilinghe19/spec_practices/blob/master/smaract.mac)

3. There are 3 spec motors used to control the devices: "test"(channel 0), "test2"(channel 1), "test3"(channel 2). "mv test 1" can be used to move the motor(channel 0). In the configuration phase, "SmarAct MCS2(Socket)" controller Type on the Devices screen and "MCS2_E" on the Motor screen to use closed-loop mode should be set. 

4. If several motors have the same controller, then it is a must to set 0/0, 0/1,... in unit/channel on the Motor screen. 
==== Install SmarActMCS2Ctrl TangoDS and SmarActMCS2Motor TangoDS  ====


1. Make new folders

  mkdir -p ~/tango/DeviceClasses/Motion/MotorControllers/Smaract/SmarActMCS2Motor
  mkdir -p ~/tango/DeviceClasses/Motion/MotorControllers/Smaract/SmarActMCS2Ctrl
  mkdir -p ~/tango/Libraries/cppserver/
2. Get the resources

  cd ~/tango/DeviceClasses/Motion/MotorControllers/Smaract/SmarActMCS2Ctrl
  svn co https://tkracht@svn.code.sf.net/p/tango-ds/code/DeviceClasses/Motion/MotorControllers/Smaract/SmarActMCS2Ctrl/tags/Release_1_1
  cd ~/tango/DeviceClasses/Motion/MotorControllers/Smaract/SmarActMCS2Motor
  svn co https://tkracht@svn.code.sf.net/p/tango-ds/code/DeviceClasses/Motion/MotorControllers/Smaract/SmarActMCS2Motor/trunk
  cd ~/tango/Libraries/cppserver 
  svn co https://tkracht@svn.code.sf.net/p/tango-ds/code/Libraries/cppserver/common
3. Compile the programs

  export TANGO_DIR=~/tango/
  cd ~/tango/DeviceClasses/Motion/MotorControllers/Smaract/SmarActMCS2Ctrl/tags/Release_1_1
  make
  cd ~/tango/DeviceClasses/Motion/MotorControllers/Smaract/SmarActMCS2Motor/trunk$ 
  make
  
 (In the Makefile of the SmarActMCS2Motor, the "PICOSCALESUPPORT ?= no" must be set. subversion should be installed in oder to use svn.)





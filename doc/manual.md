Raspswitch game console

Installation graphical 5” touch display on raspberry pi 3 revision B+

    1. Through SSH.
    2. Attached to a monitor at first time.
Choose either one of both steps before continuing to step 3

1. SSH
1.1 Find the IP of your Raspberry Pi on your LAN.
Attach raspberry pi to you network with an ethernet cable.
You need a DHCP server in your network for the raspberry pi to automatically get an IP address in your local address range.  When the raspberry pi is started it gets an IP address from the DHCP server.  You can search your LAN for the IP address of the Raspberry Pi with a network scan tool like ‘Fing’ on your pc, tablet or mobile phone.
Once you found the IP address of your Pi, make a note of it.


Replace the IP address with the IP address of your Raspberry Pi

1.2 Connect to your Raspberry Pi over SSH.
Open a terminal on your pc, mac or linux computer and SSH into the Raspberry Pi. Type the following commands to connect to your Pi.
ssh pi@<ip address raspberry pi>
When asked type the password: raspberry
Once logged in you will see the welcome screen (See picture above).
At the Bash prompt type the following command to get root (admin) access on the system.
sudo -i 
 
1.3 Download the display driver.
Type the following commands:
cd /home/pi
Make a directory to place the driver:
mkdir Displaydriver
Go into the directory you just created:
cd Displaydriver
Type the following commands to download and extract the display driver archive:
wget http://cloud.joy-it.net/index.php/s/io8CUDdxoMA7RQX/download
mv download displaydriver.tgz
tar -vzxf displaydriver.tgz

1.4 Installing the display driver
CD into the driver directory:
cd LCD-show
Intstall the display driver by executing the script as shown below:
./LCD5-show

After the installation your Raspberry Pi will reboot and the LCD screen should work now.

3 Keyboard configuration
Connect a USB keyboard to your raspberry Pi



Press <spacebar> to set all keys.




Now you can enter all keys as follow,

D-PAD UP 			> arrow up
D-PAD DOWN		> arrow down
D-PAD LEFT			> arrow left
D-PAD RIGHT			> arrow right
START				> alt left
SELECT			> alt right
A				> a  ( qwerty keyboard = q )
B				> b
X				> x
Y				> y
LEFT SHOULDER		> o
RIGHT SHOULDER		> u
LEFT TRIGGER		> p
RIGHT TRIGGER		> i
LEFT THUMB			> m ( qwerty keyboard = ; )
RIGHT THUMB		> n
LEFT ANALOG UP		> 3
LEFT ANALOG DOWN	> 4
LEFT ANALOG LEFT		> 5
LEFT ANALOG RIGHT	> 6
RIGHT ANALOG UP		> 7
RIGHT ANALOG DOWN	> 8
RIGHT ANALOG LEFT	> 9
RIGHT ANALOG RIGHT	> 0
HOTKEY ENABLE		> escape key

Press spacebar to get into the emulator.
Press left arrow key till ‘Configuration’ has been selected.
Press ‘a’ or ‘q’ on qwerty keyboard to get into configuration screen.
Press arrow down till ‘BLUETOOTH’ has been selected.
Press ‘a’ or ‘q’ on qwerty keyboard to enter menu.



Grab your left Joy-Con ®  controller and press round button on the inside of
the controller for about 5 seconds.
The leds will be moving around.



Select ‘Register and Connect to Bluetooth Device’ and press enter.



Left Joy-Con (L) has been found, press enter to attach and select
‘NoInputNoOutput’ with arrow keys and press enter.
Press after acknowledgment enter again to get in main menu.
Do exactly the same for the right Joy-Con ®  controller Joy-Con (R) 
Select in main menu ‘Cancel’ with arrow keys and press enter to get back
in the emulator. Your Joy-Con ®  controllers are configured.

Now we have to put some programs to make your controllers to work with
emulationstation.

Repeat step 1.2 to reconnect to your Raspberry Pi over SSH and gain root access.

Type the following commands at the prompt to install the necessary software modules:
cd /home/pi
mkdir JoyController
cd JoyController
wget https://github.com/DP-INVENTIONS/RASPSWITCH/raw/master/Software/JoyCtrl.py
chmod 700 JoyCtrl.py
wget https://github.com/DP-INVENTIONS/RASPSWITCH/raw/master/Software/StartJoyCtrls
chmod 700 StartJoyCtrls

aptitude install screen
aptitude install python-pip
aptitude install python-rpi.gpio
pip install python-uinput
pip install libevdev
pip install evdev



Add the following line to /etc/rc.local before the line saying ‘exit 0’ as in the example above:
/home/pi/JoyController/StartJoyCtrls &

You can enter this file by typing

pico /etc/rc.local

add line and press ctrl x keys and press Y to save and exit.

Adjust amount of GPU memory by editing /boot/config.txt



pico /boot/config.txt
Add the following line to config.txt
gpu_mem=256

Reboot your Raspberry Pi for the changes to take effect.
shutdown -r now
.

# SecureSpy
A low cost personal security surveillance system which costs only a cheap web cam and a standard computer or laptop.

##Prerequisites
- Python 2.7.x
- numpy, scipy & imutils python libraries
- OpenCV (v 3.0.0 recommended)
- x264 encoder (optional)
- Git (if you don't already have it)
- Any usb web cam
- A computer with some space for video storage

##Prequisites Installation 
- Installing Python 2.7. Refer the link below <br>
  https://www.youtube.com/watch?v=gD4eulxGNok

- Installing dependent python modules <br>
  Open command prompt or terminal and navigate to "scripts" folder within your python folder (ex: c:\python27\scripts) <br>
  Type `pip install numpy` to install numpy <br>
  Type `pip install scipy` to install scipy <br>
  Type `pip install imutils` to install imutils <br>

- Installing OpenCV
  1. On Windows <br>
  https://www.youtube.com/watch?v=EcFtefHEEII <br>
  http://docs.opencv.org/3.0-beta/doc/py_tutorials/py_setup/py_setup_in_windows/py_setup_in_windows.html

  2. On Linux <br>
  
  3. On Mac <br>
  https://www.youtube.com/watch?v=U49CVY8yOxw

- Installing x264 encoder <br>
  > Windows - Download installer from http://sourceforge.net/projects/x264vfw/ and install it. <br>
You can omit this step if you have large capacity to store videos but I highly recommend using it as it compresses video to very good extent and without any delay.
<br><br>
Possible issues without encoding: The video size may not grow beyond 4 GB and this could be a restriction of the file system or the hardware. I'm still investigating on this.

##SecureSpy Installation
Clone the files using the below command <br>
`git clone https://github.com/codecolony/SecureSpy`

##Working with SecureSpy
Just use command `python securespy.py` to run it with defaults. See next section for available options. <br>
<br>
Initially, it will ask for the background situation of the surveillance location. This is typically the scene where there is no or less movement so that the tool can capture only when there is action in the scene. Press `a` to accept the initial background frame. <br>

The tool automatically grabs a new still frame every 3 minutes by default which can be overridden (See next section). This helps with environment changes like a car stopping in the scene for hours or shadow changes due to sun movement.

Your video is stored in the current working directory with name `<timestamp>.avi` (unless you specifically use a custom name. Check next section for details).

##Options supported
- `-v ` default is `i` which stands for inbuilt webcam (ex. laptop); Use `e` for external webcam
- `-c ` default is `auto` which means automatic x264 video encoding; Use `manual` to get a list of available codec on the system to encode the video. (manual currently works only on windows)
- `-a` default is `500` which is minimum area on video activity; Smaller number means minor acivities are captured
- `-s` default is `2` which denotes video motion sensitivity; 1 = more sensitive; 5 = less sensitive
- `-r` default is `3` minutes. This controls when a new background frame needs to be grabbed.
- `-f` default is `<timestamp>.avi`. This is the output video file name.
- `-clr` default is `true`. This controls whether output video is stored in color or monochrome.
- `-fps` default is `20`. This is the frames per seconds captured in the output video.
- `-log` default is `false`. Use it to see diagnostic log messages.

ex. Running with external webcam, auto compression of video, area sensitivity of 400 pixels and total sensitivity of 1 (very sensitive) <br>
`python securespy.py -v e -c auto -a 400 -s 1`

##Current work in progress
Bug fixes and stability

##Future plans
Making UI for this tool

# SecureSpy
A low cost personal security surveilance system which costs only a cheap web cam and a standard computer or laptop.

##Prerequisites
- Python 2.7
- numpy and scipy python libraries
- OpenCV
- x264 encoder
- Any usb web cam
- A computer with some space for video storage

##Prequisites Installation 
- Installing Python 2.7. Refer the link below <br>
  https://www.youtube.com/watch?v=gD4eulxGNok

- Installing numpy and scipy modules <br>
  https://www.youtube.com/watch?v=ddpYVA-7wq4 <br>
  https://www.youtube.com/watch?v=zPMr0lEMqpo

- Installing OpenCV
  1. On Windows <br>
  https://www.youtube.com/watch?v=EcFtefHEEII <br>
  http://docs.opencv.org/3.0-beta/doc/py_tutorials/py_setup/py_setup_in_windows/py_setup_in_windows.html

  2. On Linux <br>
  
  3. On Mac <br>
  https://www.youtube.com/watch?v=U49CVY8yOxw

- Installing x264 encoder <br>
  > Windows - Download installer from http://sourceforge.net/projects/x264vfw/ and install it.

##SecureSpy Installation
Clone the files using the below command <br>
`git clone https://github.com/codecolony/SecureSpy`

##Working with SecureSpy
Just use command `python spy_windows.py` to run it with defaults. See next section for available options

##Options supported
- `-v ` default is `i` which stands for inbuilt webcam (ex. laptop); Use `e` for external webcam
- `-c ` default is `auto` which means automatic x264 video encoding; Use `manual` to get a list of available codec on the system to encode the video.
- `-a` default is `500` which is minimum area on video activity; Smaller number means minor acivities are captured
- `-s` default is `2` which denotes video motion sensitivity; 1 = more sensitive; 5 = less sensitive

ex. Running with external webcam, auto compression of video, area sensitivity of 400 pixels and total sensitivity of 1 (very sensitive) <br>
`python spy_windows.py -v e -c auto -a 400 -s 1`

##Current work in progress
Bug fixes and stability

##Future plans
Making UI for this tool

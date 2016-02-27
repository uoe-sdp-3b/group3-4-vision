# SDP-2016 
# Team B 
# Group 3-4

Vision stuff

Useful for callibration:
- colorsHSV.py: to change color internal representation
- camera.py: to change camera brightness, hue, etc
- scripts/get_camera_configuration.py is used to undistort the pitch image for the specific pitc
- test/gui_point_finder can be helpful for finding image correct transformations if the pitch image is incorrectly undistorted

ALSO NOTE:
camera settings are very dependent pitch settings:

*I think that*
3.D03 represented as 1
3.D04 represented as 0

This ALWAYS needs to be configured in a few files when you know which pitch is to be used.
Depending on the pitch settings the camera feed is undistorted in a very different way.

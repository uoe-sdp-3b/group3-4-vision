import numpy as np

# color_range['COLOR_NAME'] = ( LOWER_TRESHOLD, UPPER_TRESHOLD )

color_range = {}
color_range['white'] = ( np.array([1, 0, 100]), np.array([36, 255, 255]) )
color_range['blue'] = ( np.array([70, 50, 50]), np.array([160, 255, 255]) )
color_range['bright_blue'] = ( np.array([0, 0, 0]), np.array([0, 0, 0]) ) # TODO
color_range['pink'] = ( np.array([155, 100, 100]), np.array([175, 255, 255]) )
color_range['red'] = ( np.array([0, 110, 100]), np.array([5, 255, 255]) )
color_range['green'] = ( np.array([50, 110, 110]), np.array([70, 255, 255]) )
color_range['yellow'] = ( np.array([25, 100, 100]), np.array([40, 255, 255]) )
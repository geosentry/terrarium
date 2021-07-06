"""
Terrarium Library

The pallete module contains visualization parameters
"""
# Sentinel-2 L2A RGB Visualization Parameters
S2TC = {
    'min': 0, 
    'max': 255, 
    'bands': ['TCI_R', 'TCI_G', 'TCI_B']
}

# NDVI color palette
ndvipalette = [
    'FFFFFF', 'CE7E45', 'DF923D', 'F1B555', 'FCD163', '99B718', 
    '74A901', '66A000', '529400', '3E8601', '207401', '056201', 
    '004C00', '023B01', '012E01', '011D01', '011301'
]

# NDVI Regular Visualization Parameters
NDVIRAW = {
    'min': 0.0, 
    'max': 1.0, 
    'palette': ndvipalette
}

# NDVI Focalized Visualization Parameters
NDVIFOCAL = {
    'min': 0.0, 
    'max': 10.0, 
    'palette': ndvipalette
}

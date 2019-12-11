# Privatize the data sample using the count sketch
from .PrivCountSketch import countSketch as privCountSketch

def privatizeData(dataString):
    privCountSketch.setSketchElement(dataString)


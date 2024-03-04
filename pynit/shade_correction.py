from .import_lib import NITLibrary
import numpy
from typing import Optional

class ShadeCorrection(NITLibrary.NITUserFilter):
    correction = None
    last_image = None

    def capture(self):
        mean = numpy.mean(self.last_image)
        self.correction = self.last_image - mean

    def onNewFrame(self, frame):
        # Get a copy of the frame
        self.last_image = frame.data().copy()
        if self.correction is None:
            return self.last_image
        return (self.last_image - self.correction).clip(0.0,1.0)
        
    def get_correction(self) -> Optional[numpy.ndarray]:
        return self.correction
    
    def set_correction(self, value: Optional[numpy.ndarray]):
        self.correction = value

    def clear(self):
        self.correction = None
from .import_lib import NITLibrary
import numpy
from typing import Optional

class GainController(NITLibrary.NITUserFilter):
    low = 0.0
    high = 1.0
    last_image: Optional[numpy.ndarray] = None

    def onNewFrame(self, frame):
        self.last_image = frame.data().copy()
        delta = self.high - self.low
        return ((self.last_image - self.low) / delta).clip(0.0, 1.0)
    
    def set_range(self, low: float, high: float):
        self.low = low
        self.high = high

    def autoset(self):
        if self.last_image is None:
            self.low = 0.0
            self.high = 1.0
            return
        values = numpy.sort(self.last_image, axis=None)
        skip = len(values) // 200
        self.low = values[skip]
        self.high = values[len(values) - skip - 1]

    def get_low(self) -> float:
        return self.low
    
    def get_high(self) -> float:
        return self.high
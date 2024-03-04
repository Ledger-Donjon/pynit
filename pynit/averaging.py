from .import_lib import NITLibrary
import numpy
from typing import List

class Averaging(NITLibrary.NITUserFilter):
    def __init__(self):
        super().__init__()
        self._num = 1
        self._images: List[numpy.ndarray] = []

    def get_num(self) -> int:
        return self._num

    def set_num(self, value: int):
        self._num = value

    def restart(self):
        self._accumulator = None
        self._images: List[numpy.ndarray] = []

    def onNewFrame(self, frame: 'NITLibrary.NITFrame') -> numpy.ndarray:
        # Get a copy of the frame
        new_image = frame.data().copy()

        # Initialize accumulator (if needed)
        if len(self._images) == 0:
            self._images = [new_image]
            return new_image

        # Store the image
        self._images.append(new_image)

        # Drop extra images, keeping last ones
        if len(self._images) > self._num:
            self._images = self._images[len(self._images) - self._num:]
        
        # Return average
        return numpy.mean(self._images, axis=0, keepdims=True)

    def get_size(self) -> int:
        return len(self._images)

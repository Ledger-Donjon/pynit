from .import_lib import NITLibrary
from typing import Literal, Optional, Tuple
from .gain_controller import GainController
from .averaging import Averaging
from .shade_correction import ShadeCorrection
from .laplacian_variance import LaplacianVariance

class Observer(NITLibrary.NITUserObserver):
    last_image = None
    columns = 0
    rows = 0

    def onNewFrame(self, frame: NITLibrary.NITFrame):
        """Called by NITLibrary when a new frame has been captured by the camera."""
        self.last_image = (frame.data().copy()*255).astype('uint8').tobytes()
        self.id = frame.id()
        self.bitsPerPixel = frame.bitsPerPixel()
        self.columns = frame.columns()
        self.pixelType = frame.pixelType()
        self.rows = frame.rows()
        self.temperature = frame.temperature()
        self.timestamp = frame.timestamp()
        self.counter += 1

    def reset_counter(self):
        self.counter = 0


class PyNIT(object):
    def __init__(self):
        """
        Connect to the camera and initialize image acquisition
        """

        # Open the manager and connect to the device.
        self.manager = NITLibrary.NITManager.getInstance()

        self.device = device = self.manager.openOneDevice()
        # This should not happen, if there is not device connected, an exception should already be thrown
        if device is None:
            raise RuntimeError("No device returned")

        # Device parameters configuration.
        device.setParamValueOf("Exposure Time", "2ms" )
        device.setParamValueOf("Pixel Clock", "25MHz")

        # Data is sent to the device
        device.updateConfig()

        # Setup acquisition stream
        nuc_filename = "./nuc/25mhz/NUCFactory_2000us.yml"
        bpm_filename = "./nuc/25mhz/BPM.yml"

        device.setNucFile(nuc_filename)
        device.setBprFile(bpm_filename)

        self.averaging = Averaging()

        self.shade_correction = ShadeCorrection()

        self.gain_controller = GainController()

        self.observer = Observer()
        self.observer.reset_counter()

        self.device << self.averaging << self.shade_correction << self.gain_controller << self.observer

        # self.laplacian_variance = LaplacianVariance()
        # self.shade_correction << self.laplacian_variance
        self.device.start()


    def __del__(self):
        self.device.stop()

    def get_last_image(self) -> Tuple[int, int, Literal["L", "RGB"], Optional[bytes]]:
        """Retrieve last captured image"""
        # pynit.get_last_image returns Tuple [width, height, fmt, data], with data being None if
        # acquisition failed.
        data = self.observer.last_image
        return self.observer.columns, self.observer.rows, "L", data

    def gain_autoset(self):
        """Calculate automatically gain control parameters depending on last captured
        image. Return a tuple with calculated histogram bounds, or None if no images
        have been captured yet.
        """
        self.gain_controller.autoset()
        low = int(self.gain_controller.get_low() * 64)
        high = int(self.gain_controller.get_high() * 64)
        return low, high

    def set_gain(self, low: int, high: int):
        """Set manual gain histogram bounds."""
        if low > high:
            raise ValueError("High bound is lower than low bound!")
        if (low < 0) or (low > 0xFFFF):
            raise ValueError("Low bound out of range!")
        if (high < 0) or (high > 0xFFFF):
            raise ValueError("High bound out of range!")
        self.gain_controller.set_range(low/64.0, high/64.0)

    def set_averaging(self, value: int):
        """Set averaging image count."""
        if value < 1:
            raise ValueError("Averaging must be greater or equal to 1.")
        self.averaging.set_num(value)

    def get_averaging(self) -> int:
        """Current averaging setting."""
        return self.averaging.get_num()

    def shade_correct(self):
        """Use last captured image as base image for shading correction"""
        self.shade_correction.capture()

    def clear_shade_correction(self):
        """Clear shade correction image."""
        self.shade_correction.clear()

    def get_shade_correction(self) -> bytes:
        """Current shade correction image"""
        self.shade_correction.get_correction()

    def set_shade_correction(self, image):
        """Load a shade correction image"""
        self.shade_correction.set_correction(image)

    def get_averaged_count(self) -> int:
        return 0

    def averaging_restart(self):
        """Restart averaging."""
        pass

    def get_laplacian_std_dev(self) -> float:
        """Return standard deviation of laplacian operator on the last image."""
        return 0.0
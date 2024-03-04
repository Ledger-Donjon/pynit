from .import_lib import NITLibrary

class LaplacianVariance(NITLibrary.NITUserObserver):
    def __init__(self):
        super().__init__()
        self._result = 0.0
        # self.mutex = ???
        # double result;

    def get_result(self) -> float:
        return self._result

    def onNewFrame(self, frame: NITLibrary.NITFrame):
        return frame.data()
        #    cv::Mat dst;
        #    cv::Mat src;
        #    frame.convertTo(src, CV_16S);
        #    cv::Laplacian(src, dst, CV_16S, 3);
        #    cv::Scalar mean, std_dev;
        #    cv::meanStdDev(dst, mean, std_dev);
        #    mutex.lock();
        #    this->result = std_dev[0];
        #    mutex.unlock();

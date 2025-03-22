import os
import time
from picamera2.outputs import CircularOutput
from picamera2 import Picamera2
from config.settings import PRE_ROLL_DURATION, VIDEO_DIR
from utils.localizer import localizer


class DualCamera:
    def __init__(self):
        os.makedirs(VIDEO_DIR, exist_ok=True)

        self.cam1 = Picamera2(0)
        self.cam2 = Picamera2(1)

        config1 = self.cam1.create_video_configuration(main={"size": (1920, 1080), "format": "YUV420"})
        config2 = self.cam2.create_video_configuration(main={"size": (1920, 1080), "format": "YUV420"})

        self.cam1.configure(config1)
        self.cam2.configure(config2)

        self.buffer1 = CircularOutput(PRE_ROLL_DURATION)
        self.buffer2 = CircularOutput(PRE_ROLL_DURATION)

        self.output_path = None
        self.recording = False

    def start_prebuffering(self):
        self.cam1.start_recording(self.buffer1, encoder='h264')
        self.cam2.start_recording(self.buffer2, encoder='h264')
        localizer.print_local("camera.buffering")

    def start_recording(self):
        timestamp = int(time.time())
        self.output_path = {
            "cam1": os.path.join(VIDEO_DIR, f"cam1_{timestamp}.h264"),
            "cam2": os.path.join(VIDEO_DIR, f"cam2_{timestamp}.h264")
        }

        self.buffer1.copy_to(self.output_path["cam1"])
        self.buffer2.copy_to(self.output_path["cam2"])

        self.cam1.switch_output(self.output_path["cam1"])
        self.cam2.switch_output(self.output_path["cam2"])
        self.recording = True
        localizer.print_local("camera.started")

    def stop_recording(self):
        if self.recording:
            self.cam1.stop_recording()
            self.cam2.stop_recording()
            self.recording = False
            localizer.print_local("camera.stopped")

    def get_video_paths(self):
        return self.output_path

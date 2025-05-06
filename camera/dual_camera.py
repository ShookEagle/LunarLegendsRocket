import cv2
import time
import threading
from collections import deque
from picamera2 import Picamera2

class PrebufferedRecorder:
    def __init__(self, buffer_seconds=5, fps=30, output_path="launch_clip.h264"):
        self.buffer_seconds = buffer_seconds
        self.fps = fps
        self.output_path = output_path

        self.picam = Picamera2()
        video_config = self.picam.create_video_configuration(main={"size": (1440, 1080)})
        self.picam.configure(video_config)

        self.buffer = deque(maxlen=int(buffer_seconds * fps))
        self.running = False
        self.triggered = False
        self.recording = False
        self.lock = threading.Lock()
        self.out = None

        self.capture_thread = threading.Thread(target=self._capture_loop, daemon=True)

    def start(self):
        self.running = True
        self.picam.start()
        self.capture_thread.start()
        print("[Camera] Prebuffering started")

    def _capture_loop(self):
        while self.running:
            frame = self.picam.capture_array()
            with self.lock:
                if not self.triggered:
                    self.buffer.append(frame)
                elif self.recording:
                    self.out.write(frame)
            time.sleep(1 / self.fps)

    def trigger_save(self):
        print("[Camera] Saving prebuffer...")
        with self.lock:
            self.out = cv2.VideoWriter(
                self.output_path,
                cv2.VideoWriter_fourcc(*'H264'),
                self.fps,
                (self.buffer[0].shape[1], self.buffer[0].shape[0])
            )
            for frame in self.buffer:
                self.out.write(frame)
            self.triggered = True
        print("[Camera] Prebuffer saved")

    def continue_recording(self):
        with self.lock:
            if self.out is not None:
                self.recording = True
                print("[Camera] Continuing live recording")

    def close(self):
        print("[Camera] Shutting down...")
        self.running = False
        self.capture_thread.join()
        with self.lock:
            if self.out:
                self.out.release()
                self.out = None
        self.picam.stop()
        print("[Camera] Closed and finalized video.")

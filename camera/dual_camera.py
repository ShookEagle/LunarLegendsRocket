from picamera2 import Picamera2, Preview
import cv2
import time
import threading
from collections import deque

class PrebufferedRecorder:
    def __init__(self, buffer_seconds=5, fps=60, output_path="output.h264"):
        self.picam = Picamera2()
        self.fps = fps
        self.buffer_frames = int(buffer_seconds * fps)
        self.buffer = deque(maxlen=self.buffer_frames)
        self.output_path = output_path
        self.recording = False
        self.running = False
        self.lock = threading.Lock()

        video_config = self.picam.create_video_configuration(main={"size": (1440, 1080)})
        self.picam.configure(video_config)
        self.picam.start()

    def _capture_loop(self):
        while self.running:
            frame = self.picam.capture_array()
            with self.lock:
                self.buffer.append(frame)
            time.sleep(1 / self.fps)

    def start(self):
        self.running = True
        threading.Thread(target=self._capture_loop, daemon=True).start()

    def stop(self):
        self.running = False

    def trigger_save(self):
        print("[Camera] Triggered — saving video...")
        fourcc = cv2.VideoWriter_fourcc(*'H264')
        out = cv2.VideoWriter(self.output_path, fourcc, self.fps, (640, 480))

        with self.lock:
            for frame in list(self.buffer):
                out.write(frame)

        out.release()
        print(f"[Camera] Saved to {self.output_path}")

    def close(self):
        self.picam.stop()
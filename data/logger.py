import csv
import os
import threading
import time
from queue import Queue, Empty
from datetime import datetime
from sensors.imu import IMU
from sensors.bmp import Altimeter


class FlightLogger:

    def __init__(self,imu: IMU, bmp: Altimeter,
                 directory="logs", filename_prefix="flight", flush_interval=0.5, polling_rate=100.0):

        self.directory = directory
        os.makedirs(self.directory, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S") # reflects system boot time
        self.filename = f"{filename_prefix}_{timestamp}.csv"
        self.filepath = os.path.join(self.directory, self.filename)
        self.start_time = None

        self.imu = imu
        self.bmp = bmp

        self.file = open(self.filepath, mode="w", newline='')
        self.writer = None
        self.queue = Queue()
        self.flush_interval = flush_interval
        self.polling_rate = 1.0 / polling_rate

        self.running = False
        self.fields_set = False
        self.log_thread = threading.Thread(target=self._logging_loop, daemon=True)
        self.write_thread = threading.Thread(target=self._writer_thread, daemon=True)

    def start(self):
        print(f"[Logger] Logging to {self.filepath} at {1 / self.polling_rate} Hz")
        self.running = True
        self.log_thread.start()
        self.write_thread.start()
        self.start_time = time.time()

    def _logging_loop(self):
        while self.running:
            try:
                data = {
                    "seconds": time.time() - self.start_time,
                    "altitude": self.bmp.read_altitude(),
                    "pressure": self.bmp.read_pressure(),
                    "bmp_temp": self.bmp.read_bmp_temp(),
                    "imu_temp": self.imu.read_imu_temp(),
                    "gyro_x": self.imu.read_gyro()["x"],
                    "gyro_y": self.imu.read_gyro()["y"],
                    "gyro_z": self.imu.read_gyro()["z"],
                    "accel_x": self.imu.read_acceleration()["x"],
                    "accel_y": self.imu.read_acceleration()["y"],
                    "accel_z": self.imu.read_acceleration()["z"],
                }

                self.queue.put(data)
            except Exception as e:
                print(f"[Logger] Sensor read error: {e}")

            time.sleep(self.polling_rate)

    def _writer_thread(self):
        buffer = []
        while self.running or not self.queue.empty():
            try:
                data = self.queue.get(timeout=self.flush_interval)
                buffer.append(data)

                while not self.queue.empty():
                    buffer.append(self.queue.get_nowait())

                if buffer:
                    if not self.fields_set:
                        self.writer = csv.DictWriter(self.file, fieldnames=buffer[0].keys())
                        self.writer.writeheader()
                        self.fields_set = True

                    self.writer.writerows(buffer)
                    self.file.flush()
                    buffer.clear()

            except Empty:
                continue

    def stop(self):
        print("[Logger] Stopping...")
        self.running = False
        self.log_thread.join()
        self.write_thread.join()
        print("[Logger] Threads Joined")
        self.file.close()
        print("[Logger] File Closed")
        print("[Logger] Logging stopped.")
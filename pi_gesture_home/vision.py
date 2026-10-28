"""Optional Raspberry Pi camera and MediaPipe gesture-recognition adapter."""

from __future__ import annotations

import time
from collections.abc import Iterator
from pathlib import Path

from .models import Detection


class PiCameraGestureSource:
    """Yield detections from Picamera2 and a MediaPipe gesture model.

    Imports are delayed so simulation and tests run on non-Pi computers.
    """

    def __init__(self, model_path: str | Path, width: int = 640, height: int = 480) -> None:
        try:
            import cv2
            import mediapipe as mp
            from picamera2 import Picamera2
        except ImportError as error:
            raise RuntimeError(
                "camera mode requires Picamera2, MediaPipe, OpenCV, and NumPy; "
                "follow HARDWARE_SETUP.md"
            ) from error
        self.cv2 = cv2
        self.mp = mp
        self.camera = Picamera2()
        configuration = self.camera.create_video_configuration(
            main={"size": (width, height), "format": "RGB888"}
        )
        self.camera.configure(configuration)
        self.camera.start()
        options = mp.tasks.vision.GestureRecognizerOptions(
            base_options=mp.tasks.BaseOptions(model_asset_path=str(model_path)),
            running_mode=mp.tasks.vision.RunningMode.VIDEO,
            num_hands=1,
            min_hand_detection_confidence=0.65,
            min_tracking_confidence=0.65,
        )
        self.recognizer = mp.tasks.vision.GestureRecognizer.create_from_options(options)

    def detections(self) -> Iterator[Detection]:
        pose_names = {
            "Open_Palm": "open_palm",
            "Closed_Fist": "fist",
            "Thumb_Up": "thumbs_up",
            "Thumb_Down": "thumbs_down",
            "Pointing_Up": "pointing",
        }
        while True:
            frame = self.camera.capture_array()
            timestamp_ms = int(time.monotonic() * 1000)
            image = self.mp.Image(image_format=self.mp.ImageFormat.SRGB, data=frame)
            result = self.recognizer.recognize_for_video(image, timestamp_ms)
            if not result.gestures or not result.hand_landmarks:
                continue
            category = result.gestures[0][0]
            pose = pose_names.get(category.category_name, "unknown")
            wrist = result.hand_landmarks[0][0]
            yield Detection(timestamp_ms / 1000, pose, category.score, wrist.x, wrist.y)

    def close(self) -> None:
        self.recognizer.close()
        self.camera.stop()

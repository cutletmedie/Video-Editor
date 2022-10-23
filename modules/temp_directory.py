import os.path
import tempfile
import cv2
import numpy as np
from modules.file import get_file_type, FileTypes

# Create a temporary directory
temp_dir = tempfile.TemporaryDirectory()


def create_temp_icon(file_path:str) -> str:
    """Add a temporary icon to the temp_dir directory"""
    file_type = get_file_type(file_path)
    filename = \
        file_path.replace(".", "_").replace("\\", "/")\
        .replace("/", "_").replace(":", "")
    icon_path = temp_dir.name.replace("\\", "/") + "/" + filename + ".jpg"
    jpg_compression_param = [int(cv2.IMWRITE_JPEG_QUALITY), 20]
    if file_type == FileTypes.VIDEO:
        cap = cv2.VideoCapture(file_path)
        cap.set(1, 15)
        frame = cap.read()[1]
        cap.release()
    elif file_type == FileTypes.IMAGE:
        frame = cv2.imdecode(
            np.fromfile(file_path, dtype=np.uint8), cv2.IMREAD_COLOR)
    elif file_type == FileTypes.AUDIO:
        icon_path = os.getcwd().replace("\\", "/") + "/icons/audio_icon.png"
        return icon_path
    else:
        return ""
    dim = get_resolution(frame.shape[1], frame.shape[0])
    frame = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
    im_buf_arr = cv2.imencode('.jpg', frame, jpg_compression_param)[1]
    im_buf_arr.tofile(icon_path)
    cv2.destroyAllWindows()
    return icon_path


@staticmethod
def get_resolution(width, height):
    scale_resize = width / height
    if width > height:
        height = 200
        width = int(height * scale_resize)
    else:
        width = 200
        height = int(width / scale_resize)
    return width, height

import cv2.cv2
import subprocess

width_var = None


def getCameraLinux():
    i = 0
    device_name = []
    device_index = []
    for i in range(10):
        all_info = subprocess.getoutput(f"v4l2-ctl --device=/dev/video{i} --all")
        if not all_info.startswith("Cannot"):
            device_index.append(i)
            name_driver = all_info.split('\n')
            for j in range(len(name_driver)):
                if 'Card type' in name_driver[j]:
                    temp_name = name_driver[j].split(":")
                    temp_name = temp_name[1].split('(')
                    device_name.append(temp_name[0])

    return device_name, device_index


def getNameIndex():
    names, indexes = getCameraLinux()

    true_indexes = []
    true_names = []

    for j in range(len(indexes)):
        cap = cv2.VideoCapture(indexes[j])
        if cap.read()[0]:
            true_indexes.append(indexes[j])
            true_names.append(names[j])
            cap.release()

    return true_names, true_indexes


def getCameraWin():
    import wmi
    c = wmi.WMI()
    wql = "Select * From win32_usbControllerDevice"
    cameras = []
    for item in c.query(wql):
        a = item.Dependent.PNPClass
        b = item.Dependent.Name.upper()
        if a is not None and a.upper() == 'CAMERA' and 'AUDIO' not in b:
            cameras.append(item.Dependent.Name)
    return cameras


def getIndexWin():
    true_index = []
    i = 0
    for i in range(10):
        cap = cv2.VideoCapture(i)

        if cap.read()[0]:
            true_index.append(i)
    return true_index


def calculSize(init_width, init_height, element_type):
    global width_var
    if element_type == 'video':
        width_var = 461
    if element_type == 'image':
        width_var = 360
    height_percent = (270 / init_height)
    width_percent = (width_var / init_width)
    comp_1 = min(width_percent, height_percent)
    if comp_1 < 1:
        if init_width >= init_height and init_width > width_var:
            final_width = init_width - (init_width - width_var)
            if (init_width - width_var) > init_height or (init_width - init_width * 0.25) > init_height:
                if init_height > 270:
                    final_height = init_height - (init_height - 270)
                else:
                    final_height = init_height
            else:
                final_height = init_height - (init_width - width_var)
        else:
            final_height = init_height - (init_height - 270)
            if (init_height - 270) > init_width or (init_height - init_height * 0.25) > init_width:
                if init_width > width_var:
                    final_width = init_width - (init_width - width_var)
                else:
                    final_width = init_width
            else:
                final_width = init_width - (init_height - 270)
        return [final_width, final_height]
    else:
        return [init_width, init_height]


def writeInfoOverTime(cap):
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_c = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    duration = float((frame_c / fps))
    return duration

import time
import cv2

from _scan_for_dogs import scan_for_dogs

cap = cv2.VideoCapture(0)

def get_image_from_cam():
    ret, frame = cap.read()
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)

    return [frame, rgb]

found_dogs_count = 0
def main():
    global found_dogs_count

    count = 0
    while(True):
        print('count {}...found {} possible dogs'.format(count, found_dogs_count), end='\r')
        image_raw, rgb = get_image_from_cam()

        is_dog_response = scan_for_dogs(image_raw)

        if is_dog_response is not None:
            found_dogs_count += 1


        count += 1
        time.sleep(3)

    cap.release()
    cv2.destroyAllWindows()

main()
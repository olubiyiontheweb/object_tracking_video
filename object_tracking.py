import dlib
import cv2
import numpy as np

video = cv2.VideoCapture("people.mp4")

if video.isOpened() == False:
    print("Error opening video")

check, frame = video.read()

if check == False:
    print("Cannot read video")

cv2.imshow("first frame", frame)
cv2.waitKey(0)

bbox = cv2.selectROI(frame)


cv2.destroyAllWindows

rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

# Convert bbox to Dlib rectangle
(topLeftX, topLeftY, w, h) = bbox
bottomRightX = topLeftX + w
bottomRightY = topLeftY + h

dlibRect = dlib.rectangle(topLeftX, topLeftY,
                          bottomRightX, bottomRightY)

# Create tracker
tracker = dlib.correlation_tracker()
# Initialize tracker
tracker.start_track(rgb, dlibRect)

# Create a new window where we will display the results
cv2.namedWindow("Tracker")
# Display the first frame
cv2.imshow("Tracker", frame)

count = 0


while True:
    check, frame = video.read()

    if check == False:
        print("video cannot be read here")
        break

    # Convert frame to RGB
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # Update tracker
    tracker.update(rgb)

    count = count + 1

    objectPosition = tracker.get_position()

    topLeftX = int(objectPosition.left())

    topLeftY = int(objectPosition.top())

    bottomRightX = int(objectPosition.right())

    bottomRightY = int(objectPosition.bottom())

    # Create bounding box
    cv2.rectangle(frame, (topLeftX, topLeftY),
                  (bottomRightX, bottomRightY), (0, 0, 255), 2)

    # Display frame
    cv2.imshow("Tracker", frame)
    # print(str(video.get(cv2.CAP_PROP_FRAME_COUNT)))

    key = cv2.waitKey(2)
    if key == ord('q'):
        break
    elif key == ord('s'):
        cv2.imwrite(
            "obj_track"+str(count)+".jpg", frame)
        print("Frame Saved")

cv2.destroyAllWindows()

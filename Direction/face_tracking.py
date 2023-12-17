import cv2

def get_left_right(cap, face_detection) :
    side = "none"
    amt = 0

    ret, frame = cap.read()

    # Convert the frame to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame for face detection
    results = face_detection.process(rgb_frame)

    if results.detections:
        for detection in results.detections:
            bboxC = detection.location_data.relative_bounding_box
            x_center = bboxC.xmin + bboxC.width / 2

            # Determine if the face is on the left or right
            if x_center < 0.5:
                side = "right"
                amt = 1 - (x_center * 2)
            elif x_center > 0.5:
                side = "left"
                amt = (x_center - 0.5) * 2

    return side, amt

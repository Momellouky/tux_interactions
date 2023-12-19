import cv2 
import mediapipe as mp

class FingerCounter : 

    def __init__(self) -> None:
        self.cap = cv2.VideoCapture(0)
        self.SQUARE_WIDTH = int(640 / 2)
        self.SQUARE_HEIGHT = int(480 / 2)
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        self.mp_hands = mp.solutions.hands

    def _split24(self, image):
        # Read the image using OpenCV
        # image = cv2.imread(image_path)

        # Get image dimensions
        height, width, _ = image.shape

        # Calculate the center coordinates
        center_x = width // 2
        center_y = height // 2

        # Split the image into four quadrants
        top_left = image[0:center_y, 0:center_x]
        top_right = image[0:center_y, center_x:]
        bottom_left = image[center_y:, 0:center_x]
        bottom_right = image[center_y:, center_x:]

        return top_left, top_right, bottom_left, bottom_right
    
    def countFingers(self, cap) : 
        fingerCount = 0
        with self.mp_hands.Hands(
            model_complexity=0,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5) as hands:
            if self.cap.isOpened():
                success, image = cap.read()
                if not success:
                    print("Ignoring empty camera frame.")
                    # If loading a video, use 'break' instead of 'continue'.
                    # continue
                
                lt_image = self._split24(image)
                # To improve performance, optionally mark the image as not writeable to
                # pass by reference.
                fingerCount = 0
                for img in lt_image :
                    img.flags.writeable = False
                    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                    results = hands.process(img)

                    # Draw the hand annotations on the image.
                    img.flags.writeable = True
                    img = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

                    # Initially set finger count to 0 for each cap
                    # fingerCount = 0

                    if results.multi_hand_landmarks:

                        for hand_landmarks in results.multi_hand_landmarks:
                            # Get hand index to check label (left or right)
                            handIndex = results.multi_hand_landmarks.index(hand_landmarks)
                            handLabel = results.multi_handedness[handIndex].classification[0].label

                            # Set variable to keep landmarks positions (x and y)
                            handLandmarks = []

                            # Fill list with x and y positions of each landmark
                            for landmarks in hand_landmarks.landmark:
                                handLandmarks.append([landmarks.x, landmarks.y])

                            # Test conditions for each finger: Count is increased if finger is 
                            #   considered raised.
                            # Thumb: TIP x position must be greater or lower than IP x position, 
                            #   deppeding on hand label.
                            if handLabel == "Left" and handLandmarks[4][0] > handLandmarks[3][0]:
                                fingerCount = fingerCount+1
                            elif handLabel == "Right" and handLandmarks[4][0] < handLandmarks[3][0]:
                                fingerCount = fingerCount+1

                            # Other fingers: TIP y position must be lower than PIP y position, 
                            #   as image origin is in the upper left corner.
                            if handLandmarks[8][1] < handLandmarks[6][1]:       #Index finger
                                fingerCount = fingerCount+1
                            if handLandmarks[12][1] < handLandmarks[10][1]:     #Middle finger
                                fingerCount = fingerCount+1
                            if handLandmarks[16][1] < handLandmarks[14][1]:     #Ring finger
                                fingerCount = fingerCount+1
                            if handLandmarks[20][1] < handLandmarks[18][1]:     #Pinky
                                fingerCount = fingerCount+1

                            # Draw hand landmarks 
                            self.mp_drawing.draw_landmarks(
                                img,
                                hand_landmarks,
                                self.mp_hands.HAND_CONNECTIONS,
                                self.mp_drawing_styles.get_default_hand_landmarks_style(),
                                self.mp_drawing_styles.get_default_hand_connections_style())

                # Display finger count
                cv2.putText(image, str(fingerCount), (50, 450), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 0, 0), 10)

        return fingerCount
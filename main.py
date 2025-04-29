import cv2
import mediapipe as mp

"""
Goal of this system is when the person jump the system will measure how much height the person jump.
Using live video we need to enter the person height OR 
using any video clip we need to assume the person height eg: 1.7 meter
"""

# # Open webcam
# cap = cv2.VideoCapture(0)  

# load video clip
cap = cv2.VideoCapture(r"HeightMeasuring\sample_video.mp4")

# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

# Drawing utilities (to draw landmarks)
mp_drawing = mp.solutions.drawing_utils

highest_y = None
jump_height_meters = 0
real_height_meters = float(input("Enter your real height in meters (e.g., 1.70) = "))
pixel_height_person = None
meters_per_pixel = None

initial_frames = 50
frame_count = 0
standing_y_sum = 0
standing_y = None  

while True:
    ret, frame = cap.read()  # Read a frame

    if not ret:
        print("Failed to grab frame")
        break

    height,width,_ = frame.shape

    # Convert the image to RGB because mediapipe required 
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the RGB image to detect pose
    results = pose.process(rgb_frame)

    # If pose landmarks are detected
    if results.pose_landmarks:

        # Draw pose landmarks on the original frame
        mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        # Get the nose landmark
        nose_landmark = results.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE]
        left_heel = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HEEL]
        right_heel = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HEEL]

        # calculate average heel position
        heel_y = int(((left_heel.y + right_heel.y) / 2) * height)
        nose_y = int(nose_landmark.y * height)

        # convert normalized coordinates to pixel values
        nose_x = int(nose_landmark.x * width)
        nose_y = int(nose_landmark.y * height)

        # draw a small circle at the nose position
        cv2.circle(frame, (nose_x, nose_y), 5, (0, 255, 0), -1)
        cv2.circle(frame, (int((left_heel.x + right_heel.x)/2 * width), heel_y), 10, (255, 0, 0), -1)
         
        # measure the exact nose y coordinate in standing position  
        if standing_y is None: # collect standing_y during the first few frames
            if frame_count < initial_frames:
                standing_y_sum += nose_y
                frame_count += 1
            else:
                standing_y = standing_y_sum / initial_frames

        else:
            # extract pixel height of the person
            if pixel_height_person is None:
                pixel_height_person = heel_y - nose_y
                if pixel_height_person != 0:
                    meters_per_pixel = real_height_meters / pixel_height_person

            # update highest_y when jumping nose goes higher 
            if highest_y is None or nose_y < highest_y:
                highest_y = nose_y

            # calculate jump height
            jump_height_pixels = standing_y - highest_y

            # convert to meters
            jump_height_meters = jump_height_pixels * meters_per_pixel if meters_per_pixel else 0

            # display information
            cv2.putText(frame, f"Jump Height in Pixels : {jump_height_pixels} pixels", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 
                        1, (0, 255, 255), 1)

            cv2.putText(frame, f"Jump Height in Meters : {jump_height_meters:.2f} meters", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 
                        1, (255, 0, 255), 1)
            

    cv2.imshow('Jump Height Measurement', frame) 

    # Press 'q' to exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

print(f"jumping height in meter = {jump_height_meters:.2f}meters")

# Release the webcam and close windows
cap.release()
cv2.destroyAllWindows()

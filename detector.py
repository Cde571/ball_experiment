import cv2
import numpy as np

video_path = "C:\\Users\\caco2\\Desktop\\Sin título.mp4"
cap = cv2.VideoCapture(video_path)

# Define the new desired dimensions for the video
new_dimensions = (550, 500)

# Define the desired position and size of the rectangle
desired_position = (150, 150)
desired_width = 50
desired_height = 50

# Initialize trace variables
crossing_counter = 0 # to crossing_counter
previous_center_x = 25 # To store the previous center position
bg_subtractor = cv2.createBackgroundSubtractorMOG2()

while cap.isOpened():
    ret, frame = cap.read()

    if not ret:
        break

    # Resize the frame to the new dimensions
    frame = cv2.resize(frame, new_dimensions)
    fg_mask = bg_subtractor.apply(frame)
    # Convert the frame to HSV format
    imghsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define yellow color range in HSV format
    yellowlow = np.array([20, 50, 50], np.uint8)
    yellowhigh = np.array([32, 255, 255], np.uint8)

    # Create a mask for yellow objects
    mask_yellow = cv2.inRange(imghsv, yellowlow, yellowhigh)

    # Define green color range in HSV format
    greenlow = np.array([36, 50, 50], np.uint8)
    highgreen = np.array([75, 255, 255], np.uint8)

    # Create a mask for green objects
    mask_green = cv2.inRange(imghsv, greenlow, highgreen)

    # Define red color range in HSV format
    redlow = np.array([0, 100, 100], np.uint8)
    redhigh = np.array([40, 255, 255], np.uint8)

    # Create a mask for red objects
    mask_red = cv2.inRange(imghsv, redlow, redhigh)

    # Combine masks to detect yellow, green and red objects
    combined_mask = cv2.bitwise_or(mask_yellow, cv2.bitwise_or(mask_green, mask_red))

    # Apply the combined mask to the original frame to display the detected objects
    masked_frame = cv2.bitwise_and(frame, frame, mask=combined_mask)

    # Define the kernel for dilation
    kernel = np.ones((5, 5), np.uint8)

    # Apply dilation to the combined mask
    dilated_mask = cv2.dilate(combined_mask, kernel, iterations=1)

    # Show the frame with the dilated mask applied
    cv2.imshow('Detected Objects with Dilated Masks', masked_frame)

    # Find contours in the dilated mask
    contours, _ = cv2.findContours(dilated_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)

        # Draw rectangle around the object
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        center_x = x + w // 2
        center_y = y + h // 2

        # Check if the area of the contour is greater than 500
        if cv2.contourArea(contour) > 100:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (10, 255, 255), 1)

            # Check if the object is completely inside the desired rectangle
            if (
                    desired_position[0] <= center_x <= desired_position[0] + desired_width and
                    desired_position[1] <= center_y <= desired_position[1] + desired_height
            ):
                # Check if the object has crossed the line
                if center_x is not None and previous_center_x < 200 and center_x > 150:
                    previous_center_x +=10
                    previous_center_y = center_y
                    crossing_counter += 1 # Increment the crossing counter

        # Update the previous position of the center
        previous_center_x = center_x


    # Show the cross counter in the frame
    cv2.putText(frame, f"Crossings: {crossing_counter}", (10, 30), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 0, 0), 2)
    cv2.imshow('Detected Objects', frame)
    
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break
fg_mask = bg_subtractor.apply(frame)
cap.release()
cv2.destroyAllWindows()

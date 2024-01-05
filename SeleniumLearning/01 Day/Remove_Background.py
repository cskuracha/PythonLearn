import cv2

# Load the pre-trained background subtraction model
bg_subtractor = cv2.createBackgroundSubtractorMOG2()

# Create a video capture object
cap = cv2.VideoCapture("C:\\Users\\sagar\\OneDrive\\Documents\\Documents\\Youtube Prep\\CSAGAR-LAB\\Channel\\20231231_154858000_iOS.MOV")

# Check if the video opened successfully
if not cap.isOpened():
    print("Error opening video")
    exit()

# Define the codec and create a VideoWriter object to save the output video
fourcc = cv2.VideoWriter_fourcc(*"mp4v")  # Adjust codec for your desired format
out = cv2.VideoWriter("output_no_bg.mp4", fourcc, 20.0, (640, 480))  # Adjust resolution as needed

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    if not ret:
        print("End of video")
        break

    # Apply background subtraction
    fgmask = bg_subtractor.apply(frame)

    # Apply a threshold to create a binary mask
    thresh = cv2.threshold(fgmask, 25, 255, cv2.THRESH_BINARY)[1]

    # Apply morphological operations to refine the mask (optional)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

    # Create an inverted mask to isolate the foreground
    mask = 255 - thresh

    # Apply the mask to the original frame
    result = cv2.bitwise_and(frame, frame, mask=mask)

    # Display the resulting frame
    cv2.imshow("Background Removed", result)

    # Write the output frame to the video file
    out.write(result)

    # Exit if the 'q' key is pressed
    if cv2.waitKey(1) == ord("q"):
        break

# Release resources
cap.release()
out.release()
cv2.destroyAllWindows()

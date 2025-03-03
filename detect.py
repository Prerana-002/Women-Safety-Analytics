import cv2 
print("OpenCV imported successfully!")
print("Script is running...")

import numpy as np # type: ignore

# Load face detection model
face_proto = "models/opencv_face_detector.pbtxt"
face_model = "models/opencv_face_detector_uint8.pb"
face_net = cv2.dnn.readNet(face_model, face_proto)

# Load age detection model
age_proto = "models/age_deploy.prototxt"
age_model = "models/age_net.caffemodel"
age_net = cv2.dnn.readNet(age_model, age_proto)

# Load gender detection model
gender_proto = "models/gender_deploy.prototxt"
gender_model = "models/gender_net.caffemodel"
gender_net = cv2.dnn.readNet(gender_model, gender_proto)

# Define age and gender categories
age_list = ['(0-2)', '(4-6)', '(8-12)', '(15-20)', '(25-32)', '(38-43)', '(48-53)', '(60-100)']
gender_list = ['Male', 'Female']

# Function to detect face, age, and gender
def detect_face_age_gender(image_path):
    image = cv2.imread(image_path)
    h, w = image.shape[:2]
    
    # Prepare the input image for face detection
    blob = cv2.dnn.blobFromImage(image, 1.0, (300, 300), [104, 117, 123], swapRB=False)
    face_net.setInput(blob)
    detections = face_net.forward()

    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > 0.5:  # Threshold for face detection
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (x, y, x1, y1) = box.astype("int")

            # Extract face ROI
            face = image[y:y1, x:x1]

            # Prepare blob for age and gender prediction
            blob = cv2.dnn.blobFromImage(face, 1.0, (227, 227), [78.4263377603, 87.7689143744, 114.895847746], swapRB=False)
            
            # Predict Gender
            gender_net.setInput(blob)
            gender_preds = gender_net.forward()
            gender = gender_list[gender_preds[0].argmax()]

            # Predict Age
            age_net.setInput(blob)
            age_preds = age_net.forward()
            age = age_list[age_preds[0].argmax()]

            # Display results
            label = f"{gender}, {age}"
            cv2.putText(image, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            cv2.rectangle(image, (x, y), (x1, y1), (0, 255, 0), 2)

    # Save and show the output image
    cv2.imwrite("output.jpg", image)
    cv2.imshow("Output", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Test the function with an example image
if __name__ == "__main__":
    detect_face_age_gender("test.jpg")  # Replace with your image path

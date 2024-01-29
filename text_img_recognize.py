from flask import Flask, request, jsonify
import cv2
import easyocr
import numpy as np  # Import NumPy library
import os

app = Flask(__name__)


def preprocess_image(image):
    # Resize the image to a smaller size
    resized_image = cv2.resize(image, (0, 0), fx=0.5, fy=0.5)

    # Enhance contrast and brightness (you may need to adjust these parameters)
    enhanced_image = cv2.convertScaleAbs(resized_image, alpha=1.2, beta=30)

    return enhanced_image

def recognize_text(image):
    # Preprocess the image
    preprocessed_image = preprocess_image(image)

    # Create an OCR reader
    reader = easyocr.Reader(['en'])

    # Use easyocr to recognize text
    result = reader.readtext(preprocessed_image)

    # Extract recognized text from the result
    text = ' '.join([item[1] for item in result])

    return text

def check_text_in_data(recognized_text, data):
    # Convert recognized text to lowercase for case-insensitive comparison
    recognized_text_lower = recognized_text.lower()

    for item in data:
        chemical_name = item.get('chemical_name', '')

        if chemical_name.lower() in recognized_text_lower:
            return True, chemical_name

    return False, None

@app.route('/recognize', methods=['POST'])
def recognize_api():
    try:
        # Receive image file from the API request
        temp_image_path = 'C:/wamp64/www/Latest/eduassethub/public/'
        img_file_path = request.json['image']

        print(img_file_path)
        img_array = cv2.imread(os.path.join(temp_image_path, img_file_path))

        # Define your data as an array of objects
        data = [
            {'id': 1, 'chemical_name': 'acetone'},
            {'id': 2, 'chemical_name': 'nitric'},
            {'id': 3, 'chemical_name': 'ethanol'},
            {'id': 4, 'chemical_name': 'sodium bicarbonate'},
            {'id': 5, 'chemical_name': 'sodium chloride ar'},
            {'id': 6, 'chemical_name': 'potassium chloride'},
        ]

        # Recognize text from the image
        recognized_text = recognize_text(img_array)

        # Check if recognized text contains chemical names from the data
        contains_chemical, matched_chemical = check_text_in_data(recognized_text, data)

        if contains_chemical:
            return jsonify(matched_chemical)
        else:

            # os.remove(os.path.join(temp_image_path, img_file_path))

            return jsonify("Recognized text does not contain chemical names from the data set.")

    except Exception as e:
        return jsonify({'error': f"An error occurred: {e}"}), 500

if __name__ == '__main__':
    app.run(debug=True)

#Project Instructions

This document shows how to run the project in detail.

---

## Prerequisites
1. Make sure Python is installed in your system.
2. Use the 'requirements.txt' to install the needed Python modules.

---

## Steps to Run Project

### 1. Make sure you are in Project/Code Directory
- if not change directory to folder containing the Project/Code files.

### 2. Give the 'run.sh' Script Execution Permissions
If the script is not already executable, execute the following in the terminal:

chmod +x run.sh

### 3. Start the Application
You can run your application with:

./run.sh

Assuming everything done correctly, the script will do the following:
1. Change directory to the appropriate one.
2. Fire up the web server on 'http://127.0.0.1:5002'.
3. Output to the terminal indicating that the application is running.
---

## How to Use the Application

### 1. Open the Website
- Open your browser and go to the localhost link shown in the terminal. It is usually:

http://127.0.0.1:5002

### 2. Upload an Image
- On the homepage of webpage, you will find an upload form.
- Use the form to upload an image (upload a blurry or unclear image).

### 3. Get a clear restored Image
- Once uploaded, the application will process the image using the model and post-processing techniques.
- The processed image will be returned and displayed in the browser.

---

## Troubleshooting

1. **Python Errors:**
- Make sure Python 3 is installed and available as 'python3'.
- If any modules are missing (import erros), install them using:

pip install -r requirements.txt


2. **Website Not Opening:**
- Verify that the web Application is running and the terminal shows no errors.
- Confirm you’re using the correct localhost link, typically 'http://127.0.0.1:5002'.


3. **Image Not Processing:**
- Ensure the uploaded file is a valid image format.
- if its taking too long to process please use any other images or try images under sample inputs
- If there are specific processing errors, check the backend code in 'app.py'.


---

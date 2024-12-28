#!/bin/bash

# Navigate to the directory where app.py is located
cd web/backend || {
    echo "Directory web/backend does not exist. Please check the path.";
    exit 1;
}

# Run the app.py script
echo "Starting the application..."
python app.py

# Optional: Check if the application starts successfully
if [ $? -eq 0 ]; then
    echo "Application started successfully."
else
    echo "Failed to start the application."
    exit 1
fi

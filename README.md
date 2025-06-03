Project Title:
Image Color Extractor (Gradio Application))

Purpose: To create a user-friendly web application that allows users to upload an image and efficiently extract its most dominant colors, presenting them as a visual palette with detailed information. This project showcases practical application of image processing and machine learning (clustering) techniques.

Core Functionality:

Image Upload: Users can upload common image formats (JPG, PNG).
Dominant Color Extraction: Identifies and extracts the top N most frequently occurring (dominant) colors from the uploaded image using K-Means clustering.
Visual Color Palette: Displays the extracted colors visually as distinct color blocks.
Detailed Color Information: For each dominant color, it presents its HEX code, RGB values, and its calculated percentage of prevalence in the original image.
User Configuration: Allows users to interactively specify the number of dominant colors (N) they wish to extract (e.g., via a slider in the Gradio interface).
Technical Stack:

Frontend/Backend Framework: Gradio (for rapid prototyping and web interface deployment)
Core Logic: Python
Image Processing: Pillow (PIL Fork) for handling image files.
Clustering Algorithm: SciPy (specifically, its K-Means implementation for color quantization).
Numerical Operations: NumPy for efficient array manipulation of image pixels.


Short Description:
A Python-based web tool that utilizes K-Means clustering to identify and display the most dominant colors from any uploaded image. Built with Gradio for an interactive and accessible web interface, it's perfect for designers, artists, or anyone curious about image color composition.

Features:
Simple Image Upload: Easily upload JPG and PNG image files.
K-Means Color Quantization: Employs the K-Means algorithm to intelligently group similar colors and find the most representative ones.
Interactive Color Palette: Presents the extracted colors visually as a clean palette.
Detailed Color Data: Provides HEX codes, RGB values, and the percentage prevalence for each identified dominant color.
Adjustable Color Count: Users can dynamically control how many dominant colors (N) are extracted.
Rapid Deployment: Utilizes Gradio for quick setup and sharing as a web application.
Modular Code: Core color extraction logic is separated, allowing for easy integration into other projects or different web frameworks.
How it Works (Technical Overview):
The app.py script serves as the Gradio interface, handling file uploads and displaying results.
The color_extractor.py module contains the core logic:
An uploaded image is opened using Pillow.
The image pixels are converted into a NumPy array, suitable for numerical operations.
The scipy.cluster.vq.kmeans function is applied to the pixel data to group colors into N clusters (where N is the user-specified number of colors).
The centroids of these clusters represent the dominant colors' RGB values.
The percentage of pixels belonging to each cluster is calculated to determine the prevalence of each dominant color.
The extracted RGB values are converted to HEX codes for common web use.
The results are then passed back to the Gradio app.py to be rendered in the web interface.


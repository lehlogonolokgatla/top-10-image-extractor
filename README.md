Image Color Extractor
This repository contains a web-based tool for extracting the most dominant colors from any uploaded image. Built with Python and the Gradio library for the interactive user interface, this application leverages Pillow for image processing and SciPy (specifically K-Means clustering) to identify the prevalent colors.

Features:

Upload Any Image: Supports common image formats like JPG and PNG.
Dominant Color Extraction: Utilizes K-Means clustering to intelligently identify the most representative colors.
Customizable Output: Users can specify the number of dominant colors they wish to extract (from 1 to 20).
Visual Color Palette: Displays the extracted colors as a clear, interactive palette, showing each color's HEX code, RGB values, and its percentage prevalence in the image.
Responsive Web Interface: The Gradio interface provides a user-friendly and aesthetically pleasing experience directly in your web browser.
This project is a great example of applying data clustering techniques to image analysis and building a practical, accessible web application.

# color_extractor.py - Core logic for color extraction
from PIL import Image
import numpy as np
from scipy.cluster.vq import kmeans, vq
import webcolors
import os

def rgb_to_hex(rgb):
    """Converts an RGB tuple to a HEX string."""
    return '#%02x%02x%02x' % rgb

def get_top_n_colors(image_path, num_colors=10):
    """
    Extracts the top N most common colors from an image using K-Means clustering.

    Args:
        image_path (str): The path to the input image file.
        num_colors (int): The number of dominant colors to extract.

    Returns:
        list: A list of tuples, where each tuple contains (hex_code, rgb_tuple, percentage_of_pixels).
              Returns None if an error occurs.
    """
    if not os.path.exists(image_path):
        print(f"Error: Image file not found at '{image_path}'")
        return None

    try:
        img = Image.open(image_path)
        img = img.convert("RGB")

        pixels = np.array(img).reshape(-1, 3)

        # Handle cases where image might be too small or has too few unique colors
        # Ensure there are enough unique pixels to form num_colors clusters
        unique_pixels_count = len(np.unique(pixels, axis=0))
        actual_num_clusters = min(num_colors, unique_pixels_count)

        if actual_num_clusters == 0: # If image is completely empty or transparent after conversion
            print("No discernible colors found in the image.")
            return [] # Return an empty list if no colors can be extracted

        codebook, distortion = kmeans(pixels.astype(float), actual_num_clusters, iter=20)

        cluster_indices, min_distortions = vq(pixels, codebook)

        color_counts = np.bincount(cluster_indices, minlength=actual_num_clusters) # Ensure minlength for bincount

        total_pixels = len(pixels)
        color_percentages = (color_counts / total_pixels) * 100

        dominant_colors_info = []
        # Iterate only up to the actual number of clusters found by kmeans
        for i in range(len(codebook)): # <--- CORRECTED LINE
            rgb_tuple_float = codebook[i]
            rgb_int = tuple(np.round(rgb_tuple_float).astype(int))
            hex_code = rgb_to_hex(rgb_int)
            percentage = color_percentages[i]
            dominant_colors_info.append((hex_code, rgb_int, percentage))

        dominant_colors_info.sort(key=lambda x: x[2], reverse=True)

        return dominant_colors_info

    except FileNotFoundError:
        print(f"Error: The image file was not found at {image_path}")
        return None
    except ValueError as ve:
        # Catch specific ValueError from kmeans if input is problematic (e.g., too few unique pixels)
        print(f"ValueError during color extraction (likely too few unique colors for {num_colors} clusters): {ve}")
        return [] # Return empty list in this case
    except Exception as e:
        print(f"An unexpected error occurred during color extraction: {e}")
        return None

if __name__ == "__main__":
    # --- For local testing ---
    dummy_image_path = "test_image.png"
    if not os.path.exists(dummy_image_path):
        print(f"'{dummy_image_path}' not found. Creating a dummy test image.")
        img_array = np.zeros((100, 100, 3), dtype=np.uint8)
        img_array[:50, :50] = [255, 0, 0]    # Red
        img_array[:50, 50:] = [0, 255, 0]    # Green
        img_array[50:, :50] = [0, 0, 255]    # Blue
        # Added a 4th color to make it more interesting for tests
        img_array[50:, 50:] = [255, 255, 0]  # Yellow
        # Test with fewer colors (e.g., only one color)
        # img_array[:,:] = [100, 100, 100] # Gray image
        dummy_img = Image.fromarray(img_array)
        dummy_img.save(dummy_image_path)
        print(f"Dummy image '{dummy_image_path}' created for testing.")

    print(f"Extracting colors from {dummy_image_path}...")
    # Test with a number of colors that might be greater than actual distinct colors
    top_colors = get_top_n_colors(dummy_image_path, num_colors=10)
    if top_colors:
        print("\nTop colors found:")
        for hex_code, rgb_tuple, percentage in top_colors:
            print(f"HEX: {hex_code}, RGB: {rgb_tuple}, Percentage: {percentage:.2f}%")
    else:
        print("Failed to extract colors or no colors found.")
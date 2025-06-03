# app.py - Gradio Interface for Image Color Extractor
import gradio as gr
import os
from color_extractor import get_top_n_colors  # Import our core logic
from PIL import Image  # Import Pillow for direct image handling


def display_color_palette(image_input_pil, num_colors):  # Renamed to clearly indicate PIL Image object
    """
    Gradio interface function to process an uploaded image and display top colors.
    Takes a PIL Image object directly.
    """
    if image_input_pil is None:
        return "Please upload an image file.", "", ""

    try:
        # Save the PIL Image object to a temporary file, then pass the path to color_extractor.
        # This ensures get_top_n_colors continues to work with a file path as it expects.
        # We'll use Gradio's built-in tempfile handling for this.
        temp_image_path = "temp_uploaded_image.png"  # You can make this more unique if needed
        image_input_pil.save(temp_image_path)  # Save the PIL Image to a temporary file

        print(f"Processing image from temp file: {temp_image_path} for {num_colors} colors...")
        top_colors_info = get_top_n_colors(temp_image_path, num_colors=num_colors)

        # Clean up the temporary file immediately after processing
        os.remove(temp_image_path)

        if top_colors_info is None:
            return "Failed to extract colors. Please ensure it's a valid image and try again.", "", ""

        status_message = "Top colors extracted successfully!"

        color_blocks_html = []
        for hex_code, rgb_tuple, percentage in top_colors_info:
            r, g, b = int(rgb_tuple[0]), int(rgb_tuple[1]), int(rgb_tuple[2])

            color_block = f"""
            <div style="
                display: inline-block;
                width: 100px;
                height: 100px;
                background-color: {hex_code};
                border: 1px solid #ccc;
                margin: 5px;
                vertical-align: top;
                text-align: center;
                font-family: sans-serif;
                font-size: 0.9em;
                color: {'white' if (r * 0.299 + g * 0.587 + b * 0.114) < 186 else 'black'};
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                border-radius: 8px;
                box-shadow: 2px 2px 5px rgba(0,0,0,0.2);
            ">
                <strong>{hex_code}</strong><br>
                ({r}, {g}, {b})<br>
                {percentage:.2f}%
            </div>
            """
            color_blocks_html.append(color_block)

        combined_html = "".join(color_blocks_html)

        # Ensure that the JSON output is always a valid JSON serializable object, even if empty
        json_output = top_colors_info if top_colors_info else []
        return status_message, combined_html, json_output

    except Exception as e:
        print(f"Error in display_color_palette: {e}")
        return f"An unexpected error occurred: {e}", "", []  # Ensure JSON output is an empty list on error
        # to prevent orjson.JSONDecodeError


# Define the Gradio interface
iface = gr.Interface(
    fn=display_color_palette,
    inputs=[
        gr.Image(type="pil", label="Upload Image (JPG, PNG)", interactive=True),  # Changed type to "pil"
        gr.Slider(minimum=1, maximum=20, value=10, step=1, label="Number of Colors to Extract")
    ],
    outputs=[
        gr.Textbox(label="Status"),
        gr.HTML(label="Top Colors Palette"),
        gr.JSON(label="Raw Color Data (for debugging/dev)", visible=False)
    ],
    title="Image Color Extractor",
    description="Upload an image to identify the most dominant colors present in it. Displays HEX codes, RGB values, and their percentage prevalence."
)

# Launch the interface
if __name__ == "__main__":
    print("Launching Gradio interface. Look for the local URL in the output.")
    iface.launch(share=True)
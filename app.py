import cv2
import numpy as np
import gradio as gr


def calculate_colormask(image):
    # Convert the image to a format OpenCV can work with
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    
    # Convert image to HSV color space
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # Define range for sky colors in HSV
    lower_blue = np.array([70, 60, 60])  
    upper_blue = np.array([160, 255, 255])  

    # Threshold the HSV image to get only sky colors
    color_mask = cv2.inRange(hsv_image, lower_blue, upper_blue)

    # Find contours to identify consistent areas
    contours, _ = cv2.findContours(color_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    filtered_mask = np.zeros_like(color_mask)

    # Minimum area threshold for contours
    min_area = 50000

    # Iterate through contours and keep only the large ones
    for contour in contours:
        if cv2.contourArea(contour) > min_area:
            cv2.drawContours(filtered_mask, [contour], -1, (255), thickness=cv2.FILLED)

    return color_mask,filtered_mask




def find_uppermost_pixels(edge_image):
    rows, cols = edge_image.shape
    # Initialize with the bottom row index
    uppermost_pixels = np.full(cols, rows)  

    for col in range(cols):
        for row in range(rows):
            if edge_image[row, col] > 0:  # Check if it's an edge
                uppermost_pixels[col] = row
                break
    return uppermost_pixels




def remove_short_edges(edge_image, min_length):
    # Find all contours in the edge image
    contours, _ = cv2.findContours(edge_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    mask = np.zeros_like(edge_image)
    
    # If the contour length is greater than the minimum length, draw it on the mask
    for contour in contours:
        length = cv2.arcLength(contour, closed=False)
        if length > min_length:
            cv2.drawContours(mask, [contour], -1, (255), thickness=1)
    
    # Bitwise AND the mask with the original edge image to keep only the long edges
    filtered_edges = cv2.bitwise_and(edge_image, mask)
    
    return filtered_edges



def create_skyline_mask(filter_edges):

    skyline_row = find_uppermost_pixels(filter_edges)
    rows, cols = filter_edges.shape
    upper_sky_mask = np.zeros((rows, cols), dtype=np.uint8)

    for col, row_end in enumerate(skyline_row):
        upper_sky_mask[:row_end, col] = 255  

    return upper_sky_mask




def identify_sky(image):

    color_mask,filtered_mask = calculate_colormask(image)

    # Apply Canny edge detection 
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred_image = cv2.morphologyEx(gray_image, cv2.MORPH_OPEN, (5, 5))

    edges = cv2.Canny(blurred_image,60, 180)

    kernel = np.ones((3,3), np.uint8)
    dilated_edges = cv2.dilate(edges, kernel, iterations=10)   

    filter_edges = remove_short_edges(dilated_edges,2000)
    upper_line = find_uppermost_pixels(filter_edges)

    sky_mask = create_skyline_mask(filter_edges)
    #sky_mask = cv2.bitwise_or(skyline_mask, filtered_mask)

    sky_segmented = cv2.bitwise_and(image, image, mask=sky_mask)


    # Convert back to RGB for Gradio display
    color_mask_rgb = cv2.cvtColor(color_mask, cv2.COLOR_GRAY2BGR)
    filtered_mask_rgb = cv2.cvtColor(filtered_mask,cv2.COLOR_GRAY2BGR)
    edges_rgb = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
    filter_skyline_rgb = cv2.cvtColor(filter_edges, cv2.COLOR_GRAY2BGR)
    sky_mask_rgb = cv2.cvtColor(sky_mask, cv2.COLOR_GRAY2BGR)
    
    return color_mask_rgb,filtered_mask_rgb,edges_rgb ,filter_skyline_rgb,sky_mask_rgb,sky_segmented

demo = gr.Interface(
    fn=identify_sky,
    inputs=gr.Image(label="Original Image"),
    outputs=[gr.Image(label="color mask"),
            gr.Image(label="filter mask"), 
            gr.Image(label="edge"),
            gr.Image(label="sky line"),
            gr.Image(label="sky mask"),
            gr.Image(label="Sky Identified")
             ]
)

demo.launch(share=True)

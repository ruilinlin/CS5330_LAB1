
# Skyline Identification Demo

This project demonstrates a method for identifying the skyline in images using traditional computer vision techniques with OpenCV and Gradio. The program detects skylines in various conditions such as clear skies, cloudy weather, and during different times of the day.

## Requirements

- Python 3.x
- OpenCV-Python
- Gradio
- NumPy

## Installation

First, ensure that Python 3 is installed on your system. Then, install the required Python libraries using pip:

```bash
pip install opencv-python-headless numpy gradio
```

**Note**: We use `opencv-python-headless` instead of `opencv-python` to avoid conflicts in environments where GUI operations are not possible (like some servers).

## Running the Demo

1. Clone or download this repository to your local machine.

2. Navigate to the directory containing the code.

3. Run the Python script with the command:

   ```bash
   python app.py
   ```

4. The Gradio interface will be hosted locally and a URL will be provided in the command line to access it. 

5. Open the provided URL in a web browser to interact with the demo.

## Using the Demo

- Upload an image using the Gradio interface.
- The application will process the image and display the results, which include various masks and the identified skyline.
- You can download or interact with the output images directly in the interface.

## Features

- **Color Masking**: Identifies potential sky regions using HSV color thresholds.
- **Contour Analysis**: Refines the color mask to focus on significant sky regions.
- **Edge Detection and Dilation**: Employs Canny edge detection and dilation to make the skyline more pronounced.
- **Removal of Short Edges**: Focuses on the primary skyline by removing shorter edges.
- **Skyline Mask Creation**: Generates a mask based on the uppermost edge detected in the image.

## Contributing

Contributions to this project are welcome. Feel free to fork the repository, make changes, and submit pull requests.

## License

This project is open-source and available under the [MIT License](LICENSE).

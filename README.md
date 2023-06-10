# Remove Background

## Requirements

```
python: >3.7, <3.11
```

## Installation

```bash
pip install rembg
```

```bash
pip install -r requirements.txt
```

## Running

```bash
python final.py
```

## Working

- In 'final.py' I have created three functions `detect_and_crop_face`, `bg_remove` and `resize`.
- `detect_and_crop_face` function will detect the face in the image file using `haarcascade_frontalface_default.xml` file model and then crop it according to the country padding ratio.
- The padding ratio is calculated dividing the head_width by head_height of that country and subtracting it with 4.
- `padding_ratio = head_width/head_height - 4`
- Then `bg_remove` function will open the image frome the given path and using the remove method from `rembg` it will remove the background.
- Then create a new white background with `Image.new` and paste our removed background image over it.
- Then we save our converted image as `output.jpg`.
- This `output.jpg` is used by `resize` function which will use `imread` method to read the image.
- Then user will provide image 'width', 'height' which it will ask in milimeter(mm) then convert it to pixel and then ask for 'padding-top', 'padding-bottom', 'padding-left', 'padding-right'
  right now default is set to 20 pixels.
- Then we `resize` the image then add padding with `cv2.copyMakeBorder`.
- Finally, our output file will be saved as `padded_image.jpg`

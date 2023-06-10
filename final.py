from rembg import remove
import cv2
from PIL import Image


def detect_and_crop_face(image, faceCascade, padding_ratio):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE,
    )
    if len(faces) > 0:
        (x, y, w, h) = faces[0]
        padding_x = int(padding_ratio * w)
        padding_y = int(padding_ratio * h)
        x_start = max(0, x - padding_x)
        x_end = min(image.shape[1], x + w + padding_x)
        y_start = max(0, y - padding_y)
        y_end = min(image.shape[0], y + h + padding_y)
        cropped = image[y_start:y_end, x_start:x_end]
        return cropped
    else:
        return None


def bg_remove(img, output_path):
    remove_output = remove(img)
    output = Image.new("RGB", remove_output.size, (255, 255, 255))
    output.paste(remove_output, mask=remove_output.split()[3])
    output = output.convert("RGB")
    output.save(output_path, "JPEG")


def crop_to_aspect_ratio(aspect_ratio,
                        top_pixels,
                        bottom_pixels,
                        left_pixels,
                        right_pixels):
    img = Image.open('samples/detected_and_cropped_img.jpg')
    width, height = img.size
    desired_width = int(height * aspect_ratio)
    desired_height = int(width / aspect_ratio)
    if width/height > aspect_ratio:
        left = (width - desired_width) / 2
        top = 0
        right = (width + desired_width) / 2
        bottom = height
    else:
        left = 0
        top = (height - desired_height) / 2
        right = width
        bottom = (height + desired_height) / 2
    img = img.crop((int(left), int(top), int(right), int(bottom)))
    img.save('samples/final_output_image.jpg')
    final1 = cv2.imread("samples/final_output_image.jpg")
    country_in_pixel = ((602, 602),(413, 531),(413, 531),(413, 531))
    final = cv2.resize(final1, (country_in_pixel[int(country)-1]))
    cv2.imwrite("samples/final1.jpg", final)
    image = cv2.imread('samples/final1.jpg')
    padded_image = cv2.copyMakeBorder(
        image,
        top_pixels,
        bottom_pixels,
        left_pixels,
        right_pixels,
        cv2.BORDER_CONSTANT,
        value=(255, 255, 255),
    )
    cv2.imwrite('output_images/final.jpg', padded_image)
    final = cv2.imread("output_images/final.jpg")
    

if __name__ == "__main__":
    try:
    # country: [width, height, head_width, head_height, padding_ratio]
        all_country = {
            "1": [51, 51, 25, 35, 0.3], # USE
            "2": [35, 45, 29, 34, 0.45], # UK
            "3": [35, 45, 32, 36, 0.48], # AUSTRALIA
            "4": [35, 45, 32, 36, 0.48], # NEWZELAND
        }
        country = input(
            "Choose 1,2,3,4 according to country\n1.USA\n2.UK\n3.Australia\n4.Newzealand\n="
        )
        padding=int(input("Enter \n 1.'1' for 0 padding \n 2. '2' For 20 padding\n="))
        faceCascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )
        img_path="sample.jpeg"
        img = Image.open(img_path)
        bg_remove(img, "samples/remove_background.jpg")
        image = cv2.imread('samples/remove_background.jpg')
        cropped = detect_and_crop_face(
            image, faceCascade, all_country[country][4]
        )
        if cropped is not None:
            cv2.imwrite("samples/detected_and_cropped_img.jpg", cropped)
        width = all_country[country][0]
        height = all_country[country][1]
        if(padding==1):
            top_pixels = 0
            bottom_pixels = 0
            left_pixels = 0
            right_pixels = 0
        if(padding==2):
            top_pixels = 20
            bottom_pixels = 20
            left_pixels = 20
            right_pixels = 20

        crop_to_aspect_ratio(width/height,
                            top_pixels,
                            bottom_pixels,
                            left_pixels,
                            right_pixels
                        )
        cv2.destroyAllWindows()
    except:
        print("There is some error with the inputs")

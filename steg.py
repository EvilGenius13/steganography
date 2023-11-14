from PIL import Image, ImageDraw, ImageFont

def decode_image(path_to_png):
    # Decode image by getting size, looping over red channel pixels, and checking LSB. If LSB is 0, set pixel to black.
    
    # Open the image using PIL:
    encoded_image = Image.open(path_to_png)

    # Separate the red channel from the rest of the image:
    red_channel = encoded_image.split()[0]

    # Create a new PIL image with the same size as the encoded image:
    decoded_image = Image.new("RGB", encoded_image.size)
    pixels = decoded_image.load()
    x_size, y_size = encoded_image.size

    print(red_channel)
    for x in range(x_size):
        for y in range(y_size):
            red_value = red_channel.getpixel((x, y))

            if red_value % 2 == 0:
                pixels[x, y] = (0, 0, 0)
            else:
                pixels[x, y] = (255, 255, 255)

    # DO NOT MODIFY. Save the decoded image to disk:
    decoded_image.save("decoded_" + path_to_png)


def encode_image(path_to_png, text_to_encode):
    # Open the original image
    original_image = Image.open(path_to_png)
    encoded_image = original_image.copy()
    pixels = encoded_image.load()
    x_size, y_size = original_image.size

    # Create the text image
    text_image = write_text(text_to_encode, image_size=(x_size, y_size))
    text_pixels = text_image.load()

    # Encode the text image into the original image
    for x in range(x_size):
        for y in range(y_size):
            # Get the pixel from the text image
            text_pixel = text_pixels[x, y]

            # Get the current pixel's value from the original image
            original_pixel = list(pixels[x, y])

            # Modify the LSB of the red channel to match the text image's brightness
            lsb = 1 if text_pixel[0] > 128 else 0
            original_pixel[0] = (original_pixel[0] & ~1) | lsb

            # Update the pixel in the encoded image
            pixels[x, y] = tuple(original_pixel)

    # Save the encoded image:
    encoded_image.save("encoded_" + path_to_png)


def write_text(text_to_write, image_size=(200, 100), font_size=20):
    # Create an image with a black background
    image = Image.new('RGB', image_size, 'black')
    draw = ImageDraw.Draw(image)

    # Load a font
    font_path = "/Library/Fonts/Arial Unicode.ttf"  # Replace with the path to your font file
    font = ImageFont.truetype(font_path, font_size)

    # Set a basic position for the text
    position = (10, 10)  # Adjust as needed

    # Draw the text on the image
    draw.text(position, text_to_write, fill="white", font=font)

    return image



encode_image("tws.png", "Alright chums, (I’m back)! Let’s do this… LEEROOOOOOOOOOOOOOOOOOOOY JEEEEEENKIIIIIIIIIIINS!")
decode_image("encoded_pokemonish.png")
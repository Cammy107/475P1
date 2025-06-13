from PIL import Image

def hide_text_in_image(image_path, output_path, secret_text):
    img = Image.open(image_path)
    if img.mode != 'RGB':
        print("not RGB")
        img = img.convert('RGBA' if 'A' in img.mode else 'RGB')
    pixels = list(img.getdata())
    mode = img.mode
    secret_text += "##"
    binary_data = ''.join(format(ord(char), '08b') for char in secret_text)

    if len(binary_data) > len(pixels) * 3:
        print("Text too long!")
        return

    new_pixels = []
    data_index = 0
    for pixel in pixels:
        if len(pixel) == 4:
            r, g, b, a = pixel
        else:
            r, g, b = pixel
            a = None
        if data_index < len(binary_data):
            r = (r & ~1) | int(binary_data[data_index])
            data_index += 1
        if data_index < len(binary_data):
            g = (g & ~1) | int(binary_data[data_index])
            data_index += 1
        if data_index < len(binary_data):
            b = (b & ~1) | int(binary_data[data_index])
            data_index += 1
        if a is not None:
            new_pixels.append((r, g, b, a))
        else:
            new_pixels.append((r, g, b))

    new_img = Image.new(mode, img.size)
    new_img.putdata(new_pixels)
    new_img.save(output_path, format='PNG', optimize=False)
    print("Done")



if __name__ == "__main__":
    secret_text = """hello world"""
    hide_text_in_image("input.png", "output.png", secret_text)

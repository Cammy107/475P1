from PIL import Image

def extract_text_from_image(image_path):
    img = Image.open(image_path)
    pixels = list(img.getdata())

    binary_data = ''
    for pixel in pixels:
        for channel in pixel[:3]:
            binary_data += str(channel & 1) #extract the least significant bit

    chars = []
    for i in range(0, len(binary_data), 8):
        byte = binary_data[i:i+8] #extract ascii value
        char = chr(int(byte, 2)) #convert ascii value to char
        chars.append(char)
        if ''.join(chars[-2:]) == "##": #check the last two char
            break
    return ''.join(chars[:-2]) #remove the end sign

message = extract_text_from_image("output.png")
print(message)
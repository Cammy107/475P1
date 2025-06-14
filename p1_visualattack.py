from PIL import Image
import numpy as np

def extract_lsb_image_all_channels(image_path, Name):
    img = Image.open(image_path).convert('RGB')
    img_array = np.array(img)

    channels = ['R']
    lsb_images = []

    for i, name in enumerate(channels):
        lsb_array = img_array[:, :, i] & 1
        lsb_image = (lsb_array * 255).astype(np.uint8)
        lsb_img = Image.fromarray(lsb_image)
        lsb_img.save(f"{Name}.png")
        lsb_img.show()
        print(f"done")
        lsb_images.append(lsb_img)

    return lsb_images

if __name__ == "__main__":
    # extract_lsb_image_all_channels("input.png", "in")
    # extract_lsb_image_all_channels("output.png", "out")
    extract_lsb_image_all_channels("input.png", "input")
    for ratio in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]:
        extract_lsb_image_all_channels(f"encrypted_input_rt={ratio}.png", f"vis_atk_rt={ratio}")
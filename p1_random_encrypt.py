from PIL import Image
import random


def hide_text_in_image(image_path, output_path, secret_text, password):
    """
    使用一个密钥来随机选择像素，并将文本隐藏在图像的LSB中。

    :param image_path: 载体图像的路径。
    :param output_path: 保存隐写后图像的路径。
    :param secret_text: 要隐藏的秘密文本。
    :param password: 用于生成随机像素序列的密钥。
    """
    try:
        img = Image.open(image_path)
    except FileNotFoundError:
        print(f"错误：找不到文件 {image_path}")
        return

    # 将像素数据转换为可修改的列表
    pixels = list(img.getdata())
    mode = img.mode

    # 将像素元组列表转换为列表的列表，使其可修改
    mutable_pixels = [list(p) for p in pixels]

    # 1. 准备要嵌入的二进制数据
    # 添加结束标记，这样在提取时才知道信息在哪里结束
    secret_text += "##"  # 使用 ## 作为结束符
    binary_data = "".join(format(ord(char), "08b") for char in secret_text)

    # 2. 检查容量
    # 每个像素最多可以存储3个比特（R, G, B通道）
    max_capacity = len(pixels) * 3
    if len(binary_data) > max_capacity:
        print(
            f"错误：文本太长，无法隐藏。需要 {len(binary_data)} 比特，但容量只有 {max_capacity} 比特。"
        )
        return

    # 3. 使用密钥生成随机且可复现的像素索引序列
    pixel_indices = list(range(len(pixels)))
    random.seed(password)  # 使用密码作为种子
    random.shuffle(pixel_indices)  # 打乱像素索引的顺序

    # 4. 在随机选择的像素中嵌入数据
    data_index = 0
    for pixel_index in pixel_indices:
        # 如果所有数据都已嵌入，则提前结束循环
        if data_index >= len(binary_data):
            break

        # 获取当前要操作的像素 (注意是从 mutable_pixels 列表中获取)
        pixel = mutable_pixels[pixel_index]

        # 依次在R, G, B通道中嵌入数据
        for i in range(3):  # 遍历 R, G, B三个通道
            if data_index < len(binary_data):
                # 清除当前通道的LSB，然后将数据位写入
                pixel[i] = (pixel[i] & ~1) | int(binary_data[data_index])
                data_index += 1

    # 5. 创建并保存新图像
    # 将列表的列表转换回Image库可用的元组列表
    final_pixels = [tuple(p) for p in mutable_pixels]

    new_img = Image.new(mode, img.size)
    new_img.putdata(final_pixels)
    # 保存为无损格式PNG
    new_img.save(output_path, format="PNG", optimize=False)
    print(f"任务完成！秘密信息已使用密钥隐藏在 {output_path} 中。")


if __name__ == "__main__":

    img = Image.open("input.png")
    num_pixels = img.size[0] * img.size[1]
    base_secret_message = "Le chiffre indechiffrable."
    secret_key = "0"
    for ratio in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]:
        repeat_times = int(3 * num_pixels * ratio / (8 * len(base_secret_message))) + 1
        secret_message = base_secret_message * repeat_times

        hide_text_in_image(
            image_path="input.png",
            output_path=f"encrypted_input_rt={ratio}.png",
            secret_text=secret_message,
            password=secret_key,
        )

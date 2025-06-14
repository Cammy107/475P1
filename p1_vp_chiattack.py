import numpy as np
from PIL import Image
from scipy.stats import chi2
import matplotlib.pyplot as plt


# --- 修改后的分析脚本 ---


def plot_grayscale_histogram(image_path, output_filename):
    """
    读取图像，将其转换为灰度图，并绘制其像素值分布的直方图。
    """
    img = Image.open(image_path).convert("L")
    img_array = np.array(img)

    plt.figure(figsize=(10, 6))
    plt.hist(img_array.ravel(), bins=256, range=(0, 255), color="gray", alpha=0.8)
    plt.title(f"Grayscale Histogram for {image_path}")
    plt.xlabel("Pixel Intensity")
    plt.ylabel("Counts")
    plt.grid(True)

    plt.savefig(output_filename)
    plt.close()
    print(f"灰度直方图已保存至 {output_filename}")


def analyze_value_pairs(image_path, suspect_threshold=0.05):
    """
    对灰度图像的相邻像素值对进行卡方检测。
    这是一种更高级的隐写分析技术 (Pairs of Values - PoV)。
    """
    img = Image.open(image_path).convert("L")
    img_array = np.array(img).flatten()

    # LSB隐写会改变像素值对(2k, 2k+1)的频率，使其趋于相等
    # 卡方检验可以检测到这种非自然的均衡

    frequencies = np.zeros(256, dtype=int)
    for pixel_value in img_array:
        frequencies[pixel_value] += 1

    observed_pairs = []
    for i in range(0, 256, 2):
        if frequencies[i] + frequencies[i + 1] > 0:
            observed_pairs.append([frequencies[i], frequencies[i + 1]])

    if not observed_pairs:
        return {"chi2": 0, "p_value": 1.0, "error": "数据不足，无法进行值对分析。"}

    total_chi2 = 0
    total_dof = 0  # 自由度

    # 对每个观测频率对(O1, O2)，期望频率E是它们的平均值 E = (O1+O2)/2
    for o1, o2 in observed_pairs:
        if o1 + o2 > 0:
            expected = (o1 + o2) / 2.0
            if expected > 0:
                total_chi2 += ((o1 - expected) ** 2) / expected + (
                    (o2 - expected) ** 2
                ) / expected
                total_dof += 1

    p_value = chi2.sf(total_chi2, total_dof) if total_dof > 0 else 1.0

    return {"chi2": total_chi2, "p_value": p_value, "dof": total_dof}


def print_pair_results(image_path, results):
    print(f"\n=== {image_path} 的值对卡方检验结果 ===")
    if "error" in results:
        print(results["error"])
        return

    print(f"卡方统计量: {results['chi2']:.2f}")
    print(f"自由度: {results['dof']}")
    print(f"P-value: {results['p_value']:.4f}")

    if results["p_value"] < 0.05:
        print("结论: 值对的统计关系可能被扭曲 (P-value < 0.05)。")
        print("这很可能是LSB隐写术的一个强烈信号。🚩")
    else:
        print("结论: 值对的分布看起来很自然 (P-value >= 0.05)。")
        print("此方法未发现LSB隐写术的证据。")


if __name__ == "__main__":
    # 处理输入图像
    print("\n--- 正在分析 input.png ---")
    input_image_path = "input.png"
    plot_grayscale_histogram(input_image_path, "input_histogram.png")
    pair_results_input = analyze_value_pairs(input_image_path)
    print_pair_results(input_image_path, pair_results_input)

    print("\n" + "=" * 40 + "\n")

    # 处理输出图像
    print("--- 正在分析 encrypted_smooth_input.png ---")
    for ratio in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]:
        print(f"正在分析加密比例: {ratio}")
        output_image_path = f"encrypted_input_rt={ratio}.png"
        plot_grayscale_histogram(output_image_path, f"encrypted_input_histogram_rt={ratio}.png")
        pair_results_output = analyze_value_pairs(output_image_path)
        print_pair_results(output_image_path, pair_results_output)

import numpy as np
from PIL import Image
from scipy.stats import chi2
import matplotlib.pyplot as plt


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


def analyze_value_pairs(image_path, suspect_threshold=0.1):
    """
    通过值对卡方检验（Pairs of Values - PoV）分析图像是否存在LSB隐写。

    这种方法的核心逻辑与常规统计检验相反：
    - 自然图像的相邻像素值频率通常不相等，因此会产生一个很小的p值。
    - LSB隐写会使这些频率趋于相等，从而产生一个较大的p值。

    因此，一个“高p值”是可疑的标志。

    Args:
        image_path (str): 图像文件路径。
        suspect_threshold (float): 将图像标记为可疑的p值下限。
                                   通常取值在0.1到0.5之间。

    Returns:
        dict: 包含卡方统计量、p值、自由度和分析结论的字典。
    """
    try:
        img = Image.open(image_path).convert("L")
        img_array = np.array(img, dtype=np.int32).flatten()
    except Exception as e:
        return {"error": f"无法读取或处理图像: {e}"}

    # 统计每个像素值的频率
    # 我们将考虑(0,1), (2,3), ..., (254,255)这些值对
    observed_pairs = []
    for i in range(0, 256, 2):
        # 获取值对(2k, 2k+1)的出现次数
        n1 = np.count_nonzero(img_array == i)
        n2 = np.count_nonzero(img_array == i + 1)

        # 只有当这对值在图像中至少出现一次时，才将其纳入计算
        if n1 + n2 > 0:
            observed_pairs.append([n1, n2])

    if not observed_pairs:
        return {
            "chi2": 0,
            "p_value": 1.0,
            "dof": 0,
            "is_suspect": False,
            "conclusion": "数据不足，无法进行值对分析。",
        }

    total_chi2_statistic = 0
    degrees_of_freedom = 0

    # 对每一对观测值 (n1, n2) 进行卡方检验
    # 零假设 H0: n1 和 n2 的期望频率是相等的
    for n1, n2 in observed_pairs:
        # 期望频率是两者之和的一半
        expected = (n1 + n2) / 2.0

        # 如果期望值为0，则该对的卡方贡献为0
        if expected > 0:
            # 计算该对的卡方值: (O-E)^2/E
            pair_chi2 = ((n1 - expected) ** 2 / expected) + (
                (n2 - expected) ** 2 / expected
            )
            total_chi2_statistic += pair_chi2
            # 每对独立的检验贡献1个自由度
            degrees_of_freedom += 1

    if degrees_of_freedom == 0:
        return {
            "chi2": 0,
            "p_value": 1.0,
            "dof": 0,
            "is_suspect": False,
            "conclusion": "有效数据对不足，无法进行分析。",
        }

    # p_value 是在零假设（频率均衡）成立的情况下，
    # 获得当前或更极端卡方统计量的概率。
    # sf是生存函数 (1 - cdf)，更精确地计算右尾概率。
    p_value = chi2.sf(total_chi2_statistic, degrees_of_freedom)

    # 核心判断逻辑
    is_suspect = p_value > suspect_threshold

    conclusion = (
        f"高度可疑：检测到LSB隐写痕迹 (p值 = {p_value:.4f} > {suspect_threshold})。"
        if is_suspect
        else f"正常：未检测到明显LSB隐写痕迹 (p值 = {p_value:.4f} <= {suspect_threshold})。"
    )

    return {
        "chi2": total_chi2_statistic,
        "p_value": p_value,
        "dof": degrees_of_freedom,
        "is_suspect": is_suspect,
        "conclusion": conclusion,
    }


def print_pair_results(image_path, results):
    """
    以友好的格式打印值对卡方检验的分析结果。
    这个函数依赖 analyze_lsb_pov 函数返回的字典结构。
    """
    print(f"\n===== 对【{image_path}】的分析报告 =====")

    # 首先检查是否有错误信息
    if "error" in results:
        print(f"分析失败: {results['error']}")
        return

    # 打印核心统计数据
    # 使用 .6f 可以更精确地显示接近于0的p值
    print(f"  卡方统计量 (Chi-squared): {results['chi2']:.2f}")
    print(f"  自由度 (Degrees of Freedom): {results['dof']}")
    print(f"  P值 (P-value): {results['p_value']:.6f}")
    print("-" * 30)

    # 直接使用分析函数给出的结论
    print(f"  分析结论: {results['conclusion']}")

    # 根据 is_suspect 字段添加一个视觉提示
    if results.get("is_suspect", False):
        print("  >> 风险提示: 高 🚩")
    else:
        print("  >> 风险提示: 低 ✅")
    print("=" * 35)


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
        plot_grayscale_histogram(
            output_image_path, f"encrypted_input_histogram_rt={ratio}.png"
        )
        pair_results_output = analyze_value_pairs(output_image_path)
        print_pair_results(output_image_path, pair_results_output)

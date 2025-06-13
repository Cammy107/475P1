import numpy as np
from PIL import Image
from scipy.stats import chisquare

def analyze_lsb_distribution(image_path, alpha=0.05):
    img = Image.open(image_path).convert("RGB")
    img_array = np.array(img)
    
    results = {}
    for channel, name in enumerate(["Red", "Green", "Blue"]):
        lsb = img_array[:, :, channel] & 1
        total_bits = lsb.size
        
        count_0 = np.sum(lsb == 0)
        count_1 = total_bits - count_0
        
        pct_0 = (count_0 / total_bits) * 100
        pct_1 = (count_1 / total_bits) * 100
        
        chi2, p_value = chisquare([count_0, count_1], f_exp=[total_bits/2, total_bits/2])
        
        
        results[name] = {
            "count_0": count_0,
            "count_1": count_1,
            "pct_0": pct_0,
            "pct_1": pct_1,
            "chi2": chi2,
            "p_value": p_value,
        }
    
    return results

def print_results(results):
    for channel, data in results.items():
        print(f"\n=== {channel} Channel ===")
        print(f"0 bits: {data['count_0']} ({data['pct_0']:.2f}%)")
        print(f"1 bits: {data['count_1']} ({data['pct_1']:.2f}%)")
        print(f"Chi-square statistic: {data['chi2']:.2f}")
        print(f"P-value: {data['p_value']:.4f}")

if __name__ == "__main__":
    print("Input:")
    image_path = "input.png"
    results = analyze_lsb_distribution(image_path)
    print_results(results)
    print("Output:")
    image_path = "output.png"
    results = analyze_lsb_distribution(image_path)
    print_results(results)
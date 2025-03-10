import random
import numpy as np
import matplotlib.pyplot as plt

def calculate_detailed_delay_distribution(num_iterations=1000000):
    """
    运行 random.randint(5, 40) 指定次数，并计算详细的分布数据。

    Args:
        num_iterations: 运行次数。

    Returns:
        一个包含平均值、标准差、分位数和频率分布的字典。
    """
    delays = []
    for _ in range(num_iterations):
        delay = random.randint(5, 40)
        delays.append(delay)

    delays_array = np.array(delays)

    average_delay = np.mean(delays_array)
    std_dev = np.std(delays_array)
    percentiles = np.percentile(delays_array, [25, 50, 75])
    unique_values, counts = np.unique(delays_array, return_counts=True)

    distribution_data = {
        "average": average_delay,
        "std_dev": std_dev,
        "percentiles": {
            "25th": percentiles[0],
            "50th": percentiles[1],
            "75th": percentiles[2]
        },
        "histogram": dict(zip(unique_values, counts))
    }

    return distribution_data, delays_array

# 示例
num_iterations = 2000
distribution_data, delays_array = calculate_detailed_delay_distribution(num_iterations)

print(f"运行 {num_iterations} 次的分布数据:")
print(f"  平均延迟: {distribution_data['average']:.4f}")
print(f"  标准差: {distribution_data['std_dev']:.4f}")
print(f"  25% 分位数: {distribution_data['percentiles']['25th']:.2f}")
print(f"  中位数 (50% 分位数): {distribution_data['percentiles']['50th']:.2f}")
print(f"  75% 分位数: {distribution_data['percentiles']['75th']:.2f}")
print("  频率分布直方图:")
for value, count in distribution_data['histogram'].items():
    print(f"    {value}: {count}")

# 绘制直方图
plt.hist(delays_array, bins=range(5, 40), align='left', rwidth=0.8)
plt.xlabel("延迟值")
plt.ylabel("频率")
plt.title("延迟值频率分布直方图")
plt.show()

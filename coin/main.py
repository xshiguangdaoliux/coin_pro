import random
import matplotlib

matplotlib.use('Agg')  # 使用非交互式后端，如 'Agg'
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

# 使用中文字体 SimHei
font_properties = FontProperties(fname="C:/Windows/Fonts/simhei.ttf")


def simulate_game(teemo_sequence, yi_sequence, max_flips=10000):
    """Simulate a game where two sequences compete to appear first in a coin flip sequence."""
    flips = []
    for _ in range(max_flips):
        flip = random.choice(['正', '反'])
        flips.append(flip)

        # Check if either sequence appears in the last few flips
        if len(flips) >= 3:
            last_three = ''.join(flips[-3:])
            if last_three == yi_sequence:
                return "剑圣"
            elif last_three == teemo_sequence:
                return "提莫"
    return None


def simulate_contests(teemo_sequence, trials=100000):
    """Simulate contests between Teemo's sequence and each of Yi's remaining sequences."""
    sequences = ['正正正', '正正反', '正反正', '正反反', '反正正', '反正反', '反反正', '反反反']
    sequences.remove(teemo_sequence)  # Remove Teemo's chosen sequence from Yi's options

    results = {seq: {"剑圣胜": 0, "提莫胜": 0} for seq in sequences}

    for yi_sequence in sequences:
        for _ in range(trials):
            winner = simulate_game(teemo_sequence, yi_sequence)
            if winner:
                results[yi_sequence][f"{winner}胜"] += 1

    return results


def plot_results(teemo_sequence, results):
    """Plot bar charts for each of Yi's sequences against Teemo's choice."""
    fig, axes = plt.subplots(1, 7, figsize=(20, 5), sharey=True)
    fig.suptitle(f'剑圣与提莫的对战 - 提莫选择: {teemo_sequence}', fontproperties=font_properties)

    for ax, (yi_sequence, result) in zip(axes, results.items()):
        bars = ax.bar(result.keys(), result.values())
        ax.set_title(f'剑圣选择: {yi_sequence}', fontproperties=font_properties)
        ax.set_xlabel("胜利者", fontproperties=font_properties)
        ax.set_ylabel("胜利次数", fontproperties=font_properties)

        # 计算并在柱状图下方显示比值
        yi_wins = result["剑圣胜"]
        teemo_wins = result["提莫胜"]
        if teemo_wins > 0:
            win_ratio = f"{yi_wins / teemo_wins:.2f}"
        else:
            win_ratio = "Inf"  # 避免除零错误

        ax.text(0.5, -0.2, f"剑圣与提莫获胜次数比值: {win_ratio}", ha='center', va='top',
                transform=ax.transAxes, fontproperties=font_properties)

        # 为每个柱状图上方添加获胜次数标签
        for bar in bars:
            yval = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2, yval + 1000,  # 标签位置略高于柱状图顶部
                    int(yval), ha='center', va='bottom', fontproperties=font_properties)

        ax.tick_params(axis='x', labelrotation=0)  # 防止标签旋转影响显示
        for label in ax.get_xticklabels():
            label.set_fontproperties(font_properties)  # 设置x轴标签字体

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    # 使用提莫选择的方案和具体名称作为文件名，保持一致以覆盖原有文件
    plt.savefig(f"提莫选择的方案_{teemo_sequence}.png")
    plt.close(fig)  # 关闭图形以释放内存
    print(f"图像已保存为 '提莫选择的方案_{teemo_sequence}.png'")


# 遍历提莫的8种可能选择方案
teemo_sequences = ['正正正', '正正反', '正反正', '正反反', '反正正', '反正反', '反反正', '反反反']
for teemo_sequence in teemo_sequences:
    results = simulate_contests(teemo_sequence, trials=100000)
    plot_results(teemo_sequence, results)

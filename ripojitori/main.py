"""メインモジュール"""

import sys
from pathlib import Path
from .analyzer import DataAnalyzer


def main():
    print("=" * 50)
    print("📊 データ分析ツール v0.1.0")
    print("=" * 50)

    if len(sys.argv) < 2:
        print("\n使い方: python -m ripojitori <CSVファイルパス>")
        print("\n例: python -m ripojitori data.csv")
        return

    filepath = sys.argv[1]

    if not Path(filepath).exists():
        print(f"✗ ファイルが見つかりません: {filepath}")
        return

    analyzer = DataAnalyzer(filepath)

    if not analyzer.load_data():
        return

    summary = analyzer.get_summary()
    if summary:
        print(f"\n📋 データ概要:")
        print(f"  行数: {summary['行数']}")
        print(f"  列数: {summary['列数']}")
        print(f"  列名: {', '.join(summary['列名'])}")

    print("\n🔗 相関分析を実行中...")
    analyzer.calculate_correlation()
    analyzer.show_correlation_matrix()

    strong_corr = analyzer.find_strong_correlations(threshold=0.7)
    if strong_corr:
        print("\n⚡ 相関が強い組み合わせ（0.7以上）:")
        for pair in strong_corr:
            print(f"  • {pair['変数1']} ↔ {pair['変数2']}: {pair['相関係数']}")
    else:
        print("\n  相関が0.7以上の組み合わせはありません")

    print("\n📈 ヒートマップを生成中...")
    analyzer.plot_correlation_heatmap()

    print("\n✓ 分析が完了しました！")


if __name__ == "__main__":
    main()

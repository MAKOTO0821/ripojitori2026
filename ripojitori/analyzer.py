"""データ分析モジュール"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path


class DataAnalyzer:
    def __init__(self, filepath):
        self.filepath = Path(filepath)
        self.df = None
        self.correlation = None

    def load_data(self):
        """CSVファイルからデータを読み込む"""
        try:
            self.df = pd.read_csv(self.filepath, encoding='utf-8')
            print(f"✓ ファイルを読み込みました: {self.filepath.name}")
            print(f"  行数: {len(self.df)}, 列数: {len(self.df.columns)}")
            return True
        except Exception as e:
            print(f"✗ エラー: {e}")
            return False

    def get_summary(self):
        """データの基本情報を取得"""
        if self.df is None:
            return None

        return {
            "行数": len(self.df),
            "列数": len(self.df.columns),
            "列名": list(self.df.columns),
            "データ型": dict(self.df.dtypes)
        }

    def calculate_correlation(self):
        """数値データの相関係数を計算"""
        if self.df is None:
            print("✗ データが読み込まれていません")
            return None

        numeric_df = self.df.select_dtypes(include=[np.number])
        if numeric_df.empty:
            print("✗ 数値データが見つかりません")
            return None

        self.correlation = numeric_df.corr()
        print("✓ 相関分析が完了しました")
        return self.correlation

    def show_correlation_matrix(self):
        """相関係数マトリックスを表示"""
        if self.correlation is None:
            self.calculate_correlation()

        if self.correlation is not None:
            print("\n相関係数マトリックス:")
            print(self.correlation.round(3))

    def plot_correlation_heatmap(self, output_path="output/correlation_heatmap.png"):
        """相関係数をヒートマップで可視化"""
        if self.correlation is None:
            self.calculate_correlation()

        if self.correlation is None or self.correlation.empty:
            print("✗ 相関データが利用できません")
            return False

        output_dir = Path(output_path).parent
        output_dir.mkdir(parents=True, exist_ok=True)

        plt.figure(figsize=(10, 8))
        sns.heatmap(
            self.correlation,
            annot=True,
            fmt=".2f",
            cmap="coolwarm",
            center=0,
            square=True,
            linewidths=0.5
        )
        plt.title("相関係数ヒートマップ")
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"✓ ヒートマップを保存しました: {output_path}")
        return True

    def find_strong_correlations(self, threshold=0.7):
        """相関が強い組み合わせを検出"""
        if self.correlation is None:
            self.calculate_correlation()

        if self.correlation is None:
            return []

        strong_pairs = []
        for i in range(len(self.correlation.columns)):
            for j in range(i + 1, len(self.correlation.columns)):
                corr_value = self.correlation.iloc[i, j]
                if abs(corr_value) >= threshold:
                    strong_pairs.append({
                        "変数1": self.correlation.columns[i],
                        "変数2": self.correlation.columns[j],
                        "相関係数": round(corr_value, 3)
                    })

        return sorted(strong_pairs, key=lambda x: abs(x["相関係数"]), reverse=True)

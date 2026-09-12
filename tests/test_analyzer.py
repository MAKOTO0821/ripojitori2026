"""アナライザーのテスト"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np

sys.path.insert(0, str(Path(__file__).parent.parent))
from ripojitori.analyzer import DataAnalyzer


def test_load_data():
    """データ読み込みテスト"""
    test_csv = "tests/sample_data.csv"

    if not Path(test_csv).exists():
        print("✗ テストデータが見つかりません")
        return False

    analyzer = DataAnalyzer(test_csv)
    result = analyzer.load_data()

    if result and analyzer.df is not None:
        print("✓ データ読み込みテスト: PASSED")
        return True
    else:
        print("✗ データ読み込みテスト: FAILED")
        return False


def test_correlation():
    """相関分析テスト"""
    test_csv = "tests/sample_data.csv"

    if not Path(test_csv).exists():
        print("✗ テストデータが見つかりません")
        return False

    analyzer = DataAnalyzer(test_csv)
    analyzer.load_data()
    correlation = analyzer.calculate_correlation()

    if correlation is not None and not correlation.empty:
        print("✓ 相関分析テスト: PASSED")
        return True
    else:
        print("✗ 相関分析テスト: FAILED")
        return False


def test_summary():
    """サマリー取得テスト"""
    test_csv = "tests/sample_data.csv"

    if not Path(test_csv).exists():
        print("✗ テストデータが見つかりません")
        return False

    analyzer = DataAnalyzer(test_csv)
    analyzer.load_data()
    summary = analyzer.get_summary()

    if summary and "行数" in summary and "列数" in summary:
        print("✓ サマリー取得テスト: PASSED")
        return True
    else:
        print("✗ サマリー取得テスト: FAILED")
        return False


if __name__ == "__main__":
    print("=" * 50)
    print("🧪 ユニットテスト実行")
    print("=" * 50)

    test_load_data()
    test_correlation()
    test_summary()

    print("\n✓ テスト完了")

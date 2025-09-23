def semester_to_year(semester_code: str) -> int:
    """
    將學期編號字串轉換成西元年份
    例如: '113-2' -> 2015
    嚴格檢查：
        - 學年度須為正整數（民國年）
        - 學期只能為 1 或 2
    """
    try:
        academic_year_str, term_str = semester_code.split('-')

        # 檢查學年度
        if not academic_year_str.isdigit():
            raise ValueError("學年度必須是數字")
        academic_year = int(academic_year_str)
        if academic_year <= 0:
            raise ValueError("學年度必須是正整數（民國年）")

        # 檢查學期
        if term_str not in {"1", "2"}:
            raise ValueError("學期只能為 '1' 或 '2'")
        term = int(term_str)

        year = academic_year + 1911
        if term == 2:  # 下學期在隔年
            year += 1
        return year

    except (ValueError, IndexError) as e:
        raise ValueError(f"學期編號格式錯誤: {e}\n正確格式如 '113-1' 或 '113-2'")

# 測試
print(semester_to_year("113-2"))  # 2015
print(semester_to_year("113-1"))  # 2014
print(semester_to_year("0-1"))    # ❌ ValueError
print(semester_to_year("113-3"))  # ❌ ValueError
print(semester_to_year("abc-2"))  # ❌ ValueError

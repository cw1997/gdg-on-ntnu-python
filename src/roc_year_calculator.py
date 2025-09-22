def calculate_roc_year(gregorian_year):
    """
    Convert a Gregorian year to the Republic of China (ROC) year.

    Parameters:
    gregorian_year (int): The Gregorian year to convert.

    Returns:
    int: The corresponding ROC year.
    """
    if gregorian_year < 1912: # ROC calendar starts from 1912
        print("Gregorian year must be 1912 or later.")
        return None
    else:
        return gregorian_year - 1911

if __name__ == "__main__":
    year = int(input())
    roc_year = calculate_roc_year(year)
    print(f"The ROC year for {year} is {roc_year}.")

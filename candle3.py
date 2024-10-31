import pandas as pd

# Define the contractor's phone number as a string
CONTRACTOR_PHONE_NUMBER = "332-274-4185"


def find_contractor_neighbourhood(customers_path, contractor_phone):
    """Find the neighbourhood of the contractor based on their phone number."""
    customers = pd.read_csv(customers_path)
    contractor_neighbourhood = customers.loc[customers["phone"]
                                             == contractor_phone, "citystatezip"].iloc[0]
    return contractor_neighbourhood


def filter_customers_by_neighbourhood(customers_path, neighbourhood):
    """Filter customers based on the specified neighborhood."""
    customers_df = pd.read_csv(customers_path)
    customers_in_neighbourhood = customers_df[customers_df["citystatezip"]
                                              == neighbourhood]
    customers_in_neighbourhood["birthdate"] = pd.to_datetime(
        customers_in_neighbourhood["birthdate"], errors='coerce')
    return customers_in_neighbourhood


def filter_by_chinese_year_and_zodiac(customers):
    """Filter customers by Chinese Year (Year of the Rabbit) and Cancer Zodiac Sign."""
    years_of_rabbit = [1915, 1927, 1939, 1951,
                       1963, 1975, 1987, 1999, 2011, 2023]

    year_match = customers[customers["birthdate"].dt.year.isin(
        years_of_rabbit)]

    year_match["birth_month"] = year_match["birthdate"].dt.month
    year_match["birth_day"] = year_match["birthdate"].dt.day

    cancer_customers = year_match[
        ((year_match["birth_month"] == 6) & (year_match["birth_day"] >= 21)) |
        ((year_match["birth_month"] == 7) & (year_match["birth_day"] <= 22))
    ]
    return cancer_customers


if __name__ == "__main__":
    customers_path = "./data/noahs-customers.csv"

    contractor_neighbourhood = find_contractor_neighbourhood(
        customers_path, CONTRACTOR_PHONE_NUMBER)

    if contractor_neighbourhood:

        neighborhood_customers = filter_customers_by_neighbourhood(
            customers_path, contractor_neighbourhood)

        final_candidates = filter_by_chinese_year_and_zodiac(
            neighborhood_customers)

        print("Potential Candidate(s) for the Rug Recipient:")
        print(final_candidates[['name', 'phone', 'citystatezip']])
    else:
        print("Contractor's neighborhood not found.")

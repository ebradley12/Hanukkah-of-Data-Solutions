# pylint: disable=redefined-outer-name

"""Import libraries"""
import pandas as pd


def find_sku(products_path):
    """Load products data and find the SKU for 'Rug Cleaner'."""
    products_df = pd.read_csv(products_path)
    sku_row = products_df[products_df['desc'] == 'Rug Cleaner']
    return sku_row.iloc[0]['sku']


def find_order_ids_by_sku(order_details_path, sku):
    """Find all order IDs containing the specified SKU."""
    orders_df = pd.read_csv(order_details_path)
    sku_match = orders_df[orders_df['sku'] == sku]
    order_ids = set(sku_match['orderid'])
    return order_ids


def filter_orders_by_year_and_ids(orders_path, year, order_ids):
    """Filter Noah's orders by year and matching order IDs and return matching customer IDs."""
    order_df = pd.read_csv(orders_path)
    order_df["ordered"] = pd.to_datetime(order_df['ordered'])

    order_id_match = order_df[(order_df['orderid'].isin(order_ids))]

    year_match = order_id_match[(order_id_match['ordered'].dt.year == year)]
    customer_ids = set(year_match['customerid'])
    return customer_ids


def filter_customers(customers_path, customer_ids, initials):
    """Filter customers by customer_ids and initials JP."""
    customers_df = pd.read_csv(customers_path)
    customer_id_match = customers_df[(
        customers_df['customerid'].isin(customer_ids))]

    customer_id_match['first_initial'] = customer_id_match['name'].apply(
        lambda x: x.split()[0][0].upper())
    print(customer_id_match['first_initial'])
    customer_id_match['last_initial'] = customer_id_match['name'].apply(
        lambda x: x.split()[-1][0].upper())
    first_initial, last_initial = initials[0], initials[1]
    contractor_candidates = customer_id_match[(customer_id_match['first_initial'] == first_initial)
                                              & (customer_id_match['last_initial'] == last_initial)]
    return contractor_candidates


if __name__ == "__main__":
    sku = find_sku("./data/noahs-products.csv")
    order_ids = find_order_ids_by_sku("./data/noahs-orders_items.csv", sku)
    customer_ids = filter_orders_by_year_and_ids(
        "./data/noahs-orders.csv", 2017, order_ids)
    matching_customer = filter_customers(
        "./data/noahs-customers.csv", customer_ids, "JP")
    phone_number = matching_customer["phone"]
    print(phone_number)

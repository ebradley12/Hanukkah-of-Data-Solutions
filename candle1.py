"""Import libraries"""
import pandas as pd


def extract_last_name(name):
    """Extract the last name from a full name string."""
    return name.split()[-1]


def name_to_phone(name):
    """Convert a last name to a phone number based on letter-to-digit mapping."""
    letter_to_digit_mapping = {
        'A': '2', 'B': '2', 'C': '2',
        'D': '3', 'E': '3', 'F': '3',
        'G': '4', 'H': '4', 'I': '4',
        'J': '5', 'K': '5', 'L': '5',
        'M': '6', 'N': '6', 'O': '6',
        'P': '7', 'Q': '7', 'R': '7', 'S': '7',
        'T': '8', 'U': '8', 'V': '8',
        'W': '9', 'X': '9', 'Y': '9', 'Z': '9'
    }
    return ''.join(letter_to_digit_mapping.get(char.upper(), '') for char in name)


def find_investigator(df):
    """Identify the investigator by matching phone numbers generated from last names."""
    df['last_name'] = df['name'].apply(extract_last_name)
    df['generated_phone'] = df['last_name'].apply(name_to_phone)
    df['phone_numbers'] = df['phone'].apply(lambda x: x.replace("-", ""))
    df['match'] = df['generated_phone'] == df['phone_numbers']
    investigator = df[df['match']]
    print(investigator[['customerid', 'name', 'last_name',
          'phone', 'generated_phone', 'phone_numbers']])

    return investigator[['customerid', 'name', 'phone']]


if __name__ == "__main__":
    customer_data = pd.read_csv("./5784/noahs-customers.csv")
    investigator_details = find_investigator(customer_data)
    print(f"Investigator's Details: {investigator_details}")

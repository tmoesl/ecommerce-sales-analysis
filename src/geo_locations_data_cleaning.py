# Import necessary libraries
import pandas as pd


# Define the function to clean the geo locations data
def clean_geo_locations_data(base_path):
    """
    Cleans the geo locations data by dropping duplicates, filling null values, adding country names, and altering region values.
    """
    # Define paths dynamically
    input_file = base_path / "data/processed/geo_locations.csv"
    output_file = base_path / "data/cleaned/geo_locations_cleaned.csv"

    # Load data
    df = pd.read_csv(input_file)
    initial_rows = df.shape[0]
    print(f"Original dimensions {df.shape}\n")  # 193, 2

    # ----------------------------
    # DUPLICATES ON PRIMARY KEY
    # ----------------------------

    # Drop duplicates on primary key [# 1]
    df = df.drop_duplicates(subset=["country_code"], keep="last")
    print(f"Dimensions after dropping duplicates: {df.shape}\n")

    # ----------------------------
    # NULL VALUES
    # ----------------------------

    # Check for null values [# 1, 26]
    nullvalues = df.isnull().sum()
    print(f"Null-Values: \n{nullvalues}\n")

    # Country mapping dictionary to fill NaN values
    region_mapping = {
        "AG": "LATAM",
        "AI": "LATAM",
        "AW": "LATAM",
        "BB": "LATAM",
        "BJ": "EMEA",
        "BM": "LATAM",
        "BQ": "LATAM",
        "BS": "LATAM",
        "BZ": "LATAM",
        "CA": "NA",
        "CW": "LATAM",
        "GD": "LATAM",
        "GL": "EMEA",
        "GP": "LATAM",
        "JM": "LATAM",
        "KN": "LATAM",
        "KY": "LATAM",
        "LC": "LATAM",
        "MQ": "LATAM",
        "PR": "LATAM",
        "SX": "LATAM",
        "TC": "LATAM",
        "TT": "LATAM",
        "VC": "LATAM",
        "VG": "LATAM",
        "VI": "LATAM",
    }

    # Fill NaN based on mapping dictionary
    df["region"] = df["region"].fillna(df["country_code"].replace(region_mapping))
    df.loc[129, "country_code"] = "NA"

    # Country mapping dictionary to alter region values
    country_mapping = {
        "AM": "EMEA",
        "AZ": "EMEA",
        "RU": "EMEA",
        "UZ": "EMEA",
        "US": "NA",
    }

    # Alter region values based on mapping dictionary
    df["region"] = df["region"].mask(
        df["country_code"].isin(country_mapping.keys()),
        df["country_code"].map(country_mapping),
    )

    # ----------------------------
    # UNIQUE VALUES
    # ----------------------------

    # Check unique values
    nuniq = df.nunique()
    print(f"Unique values: \n{nuniq}\n")

    # ----------------------------
    # COUNTRY NAMES
    # ----------------------------

    # Country mapping dictionary to add country names
    country_mapping = {
        "AD": "Andorra",
        "AE": "United Arab Emirates",
        "AG": "Antigua and Barbuda",
        "AI": "Anguilla",
        "AL": "Albania",
        "AM": "Armenia",
        "AO": "Angola",
        "AR": "Argentina",
        "AS": "American Samoa",
        "AT": "Austria",
        "AU": "Australia",
        "AW": "Aruba",
        "AX": "Aland Islands",
        "AZ": "Azerbaijan",
        "BA": "Bosnia and Herzegovina",
        "BB": "Barbados",
        "BD": "Bangladesh",
        "BE": "Belgium",
        "BF": "Burkina Faso",
        "BG": "Bulgaria",
        "BH": "Bahrain",
        "BJ": "Benin",
        "BM": "Bermuda",
        "BN": "Brunei Darussalam",
        "BO": "Bolivia",
        "BQ": "Bonaire, Sint Eustatius and Saba",
        "BR": "Brazil",
        "BS": "Bahamas",
        "BT": "Bhutan",
        "BW": "Botswana",
        "BY": "Belarus",
        "BZ": "Belize",
        "CA": "Canada",
        "CD": "Congo (Democratic Republic)",
        "CH": "Switzerland",
        "CI": "Cote d'Ivoire",
        "CK": "Cook Islands",
        "CL": "Chile",
        "CM": "Cameroon",
        "CN": "China",
        "CO": "Colombia",
        "CR": "Costa Rica",
        "CU": "Cuba",
        "CV": "Cabo Verde",
        "CW": "Curacao",
        "CY": "Cyprus",
        "CZ": "Czechia",
        "DE": "Germany",
        "DK": "Denmark",
        "DO": "Dominican Republic",
        "DZ": "Algeria",
        "EC": "Ecuador",
        "EE": "Estonia",
        "EG": "Egypt",
        "ES": "Spain",
        "ET": "Ethiopia",
        "FI": "Finland",
        "FJ": "Fiji",
        "FO": "Faroe Islands",
        "FR": "France",
        "GB": "United Kingdom",
        "GD": "Grenada",
        "GE": "Georgia",
        "GF": "French Guiana",
        "GG": "Guernsey",
        "GH": "Ghana",
        "GI": "Gibraltar",
        "GL": "Greenland",
        "GN": "Guinea",
        "GP": "Guadeloupe",
        "GR": "Greece",
        "GT": "Guatemala",
        "GU": "Guam",
        "GY": "Guyana",
        "HK": "Hong Kong",
        "HN": "Honduras",
        "HR": "Croatia",
        "HT": "Haiti",
        "HU": "Hungary",
        "ID": "Indonesia",
        "IE": "Ireland",
        "IL": "Israel",
        "IM": "Isle of Man",
        "IN": "India",
        "IQ": "Iraq",
        "IR": "Iran",
        "IS": "Iceland",
        "IT": "Italy",
        "JE": "Jersey",
        "JM": "Jamaica",
        "JO": "Jordan",
        "JP": "Japan",
        "KE": "Kenya",
        "KG": "Kyrgyzstan",
        "KH": "Cambodia",
        "KN": "Saint Kitts and Nevis",
        "KR": "South Korea",
        "KW": "Kuwait",
        "KY": "Cayman Islands",
        "KZ": "Kazakhstan",
        "LA": "Laos",
        "LB": "Lebanon",
        "LC": "Saint Lucia",
        "LI": "Liechtenstein",
        "LK": "Sri Lanka",
        "LT": "Lithuania",
        "LU": "Luxembourg",
        "LV": "Latvia",
        "MA": "Morocco",
        "MC": "Monaco",
        "MD": "Moldova",
        "ME": "Montenegro",
        "MG": "Madagascar",
        "MH": "Marshall Islands",
        "MK": "North Macedonia",
        "ML": "Mali",
        "MM": "Myanmar",
        "MN": "Mongolia",
        "MO": "Macao",
        "MP": "Northern Mariana Islands",
        "MQ": "Martinique",
        "MR": "Mauritania",
        "MT": "Malta",
        "MU": "Mauritius",
        "MV": "Maldives",
        "MW": "Malawi",
        "MX": "Mexico",
        "MY": "Malaysia",
        "MZ": "Mozambique",
        "NA": "Namibia",
        "NC": "New Caledonia",
        "NG": "Nigeria",
        "NI": "Nicaragua",
        "NL": "Netherlands",
        "NO": "Norway",
        "NP": "Nepal",
        "NZ": "New Zealand",
        "OM": "Oman",
        "PA": "Panama",
        "PE": "Peru",
        "PF": "French Polynesia",
        "PG": "Papua New Guinea",
        "PH": "Philippines",
        "PK": "Pakistan",
        "PL": "Poland",
        "PR": "Puerto Rico",
        "PS": "Palestine",
        "PT": "Portugal",
        "PY": "Paraguay",
        "QA": "Qatar",
        "RE": "Reunion",
        "RO": "Romania",
        "RS": "Serbia",
        "RU": "Russia",
        "RW": "Rwanda",
        "SA": "Saudi Arabia",
        "SC": "Seychelles",
        "SD": "Sudan",
        "SE": "Sweden",
        "SG": "Singapore",
        "SI": "Slovenia",
        "SK": "Slovakia",
        "SL": "Sierra Leone",
        "SN": "Senegal",
        "SO": "Somalia",
        "SV": "El Salvador",
        "SX": "Sint Maarten",
        "TC": "Turks and Caicos Islands",
        "TG": "Togo",
        "TH": "Thailand",
        "TJ": "Tajikistan",
        "TL": "Timor-Leste",
        "TN": "Tunisia",
        "TR": "Turkey",
        "TT": "Trinidad and Tobago",
        "TW": "Taiwan",
        "TZ": "Tanzania",
        "UA": "Ukraine",
        "UG": "Uganda",
        "US": "United States",
        "UY": "Uruguay",
        "UZ": "Uzbekistan",
        "VC": "Saint Vincent and the Grenadines",
        "VE": "Venezuela",
        "VG": "British Virgin Islands",
        "VI": "U.S. Virgin Islands",
        "VN": "Vietnam",
        "VU": "Vanuatu",
        "YE": "Yemen",
        "ZA": "South Africa",
        "ZM": "Zambia",
        "ZW": "Zimbabwe",
    }

    # Add country names to the dataframe
    df.insert(1, "country_name", df["country_code"].map(country_mapping))

    # ----------------------------
    # SAVE TO CSV
    # ----------------------------

    # Save cleaned data to CSV [# 192, 3]
    final_rows = df.shape[0]
    print(f"Rows dropped during cleaning: {initial_rows - final_rows}")  # 1
    print(f"Final dimensions: {df.shape}")
    df.to_csv(output_file, index=False, encoding="utf-8")

import argparse
import csv
import json

fieldnames = ["name",
        "given_name",
        "family_name",
        "middle_name",
        "nickname",
        "preferred_username",
        "profile",
        "picture",
        "website",
        "email",
        "email_verified",
        "gender",
        "birthdate",
        "zoneinfo",
        "locale",
        "phone_number",
        "phone_number_verified",
        "address",
        "updated_at",
        "cognito:mfa_enabled",
        "cognito:username"]


def convert(source_json_file, target_csv_file):
    with open(source_json_file, 'r') as j_file, open(target_csv_file, 'w') as c_file:
        j_user_list = json.load(j_file)
        csv_writer = csv.DictWriter(c_file, fieldnames=fieldnames)
        csv_writer.writeheader()
        for j_user in j_user_list:
            user_dict = {}
            user_dict['cognito:username'] = j_user.get('Username')
            user_dict['cognito:mfa_enabled'] = "false"
            user_dict['phone_number_verified'] = "false"
            attrs = j_user.get('Attributes')
            for attr in attrs:
                if attr.get('Name') == 'email':
                    user_dict['email'] = attr.get('Value')
                if attr.get('Name') == 'email_verified':
                    user_dict['email_verified'] = attr.get('Value')
                
            csv_writer.writerow(user_dict)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('input_json', type=str)
    parser.add_argument('output_csv', type=str)
    args = parser.parse_args()
    convert(args.input_json, args.output_csv)

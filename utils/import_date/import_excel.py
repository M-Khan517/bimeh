import pandas as pd
from apps.account_module.models import User, SubUser


def import_data(path: str):
    df = pd.read_excel(path)

    users = User.objects.all()
    subs = SubUser.objects.all()

    excel_subUsers = []
    not_found_phones = []

    for _, row in df.iterrows():
        phone = f"0{row['phone']}"
        get_manager = users.filter(phone=phone).first()

        if not get_manager:
            not_found_phones.append(phone)
            continue

        sub_names = str(row.get("user_full_name", "")).split(",")
        national_codes = str(row.get("user_national_code", "")).split(",")

        sub_names = [
            str(name).strip()
            for name in sub_names
            if pd.notna(name) and str(name).strip()
        ]
        national_codes = [
            str(code).strip()
            for code in national_codes
            if pd.notna(code) and str(code).strip()
        ]

        length = min(len(sub_names), len(national_codes))

        for i in range(length):
            name = sub_names[i]
            code = national_codes[i]

            if not subs.filter(national_code=code).exists():
                excel_subUsers.append(
                    SubUser(manager=get_manager, full_name=name, national_code=code)
                )
                print(f"{i} - {name}")

    if excel_subUsers:
        SubUser.objects.bulk_create(excel_subUsers)

    if not_found_phones:
        with open("log.txt", "a") as f:
            for phone in not_found_phones:
                f.write(f"\nmanager not found: {phone}")

    print("end")

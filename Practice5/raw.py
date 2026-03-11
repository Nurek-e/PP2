import re
import json

with open(r"C:\Users\nural\OneDrive\Рабочий стол\pp2\Practice5\raw.txt", "r", encoding="utf-8") as f:
    text = f.read()

date_time_match = re.search(r"Время:\s*(\d{2}\.\d{2}\.\d{4}\s+\d{2}:\d{2}:\d{2})", text)
date_time = date_time_match.group(1) if date_time_match else ""

payment_match = re.search(r"(Банковская карта|Наличные|Карта):", text)
payment_method = payment_match.group(1) if payment_match else ""

total_match = re.search(r"ИТОГО:\s*\n?\s*([\d\s]+,\d{2})", text)
total_amount = total_match.group(1).replace(" ", "") if total_match else ""

prices = re.findall(r"\b\d[\d\s]*,\d{2}\b", text)
prices = [p.replace(" ", "") for p in prices]

product_matches = re.findall(
    r"\d+\.\s*\n(.+?)\n\d+,\d+\s*x\s*([\d\s]+,\d{2})\n([\d\s]+,\d{2})",
    text
)

products = []
for name, unit_price, total_price in product_matches:
    products.append({
        "name": name.strip(),
        "unit_price": unit_price.replace(" ", ""),
        "total_price": total_price.replace(" ", "")
    })

result = {
    "date_time": date_time,
    "payment_method": payment_method,
    "total_amount": total_amount,
    "all_prices": prices,
    "products": products
}

print(json.dumps(result, ensure_ascii=False, indent=4))
import json
import os

current_dir = os.path.dirname(__file__)


file_path = os.path.join(current_dir, "sample-data.json")


with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

items = data["imdata"]

print("Interface Status")
print("=" * 80)
print(f"{'DN':50} {'Description':20} {'Speed':6} {'MTU':6}")
print("-" * 80)

for item in items:
    attrs = item["l1PhysIf"]["attributes"]

    dn = attrs["dn"]
    descr = attrs["descr"]
    speed = attrs["speed"]
    mtu = attrs["mtu"]

    print(f"{dn:50} {descr:20} {speed:6} {mtu:6}")

import requests
import json
from dateutil.parser import parse

devices = {
    "device1": "iPhone",
    "device2": "iPad",
    "device3": "Mac"
}

for device_key, device_name in devices.items():
    device_url = f"https://www.betahub.cn/api/apple/devices/{device_name}"
    response = requests.get(device_url)
    devices_data = response.json()

    all_data = []

    for device in devices_data:
        identifier = device.get("identifier")

        url1 = f"https://www.betahub.cn/api/apple/firmwares/{identifier}?type=1"
        url2 = f"https://www.betahub.cn/api/apple/firmwares/{identifier}?type=2"

        response1 = requests.get(url1)
        data1 = response1.json()

        release_date_str = data1.get("release_date")
        release_date_obj = parse(release_date_str)
        formatted_release_date = release_date_obj.strftime("%Y.%m.%d")

        filtered_data1 = {
            "id": data1.get("id"),
            "name": data1.get("name"),
            "identifier": data1.get("identifier"),
            "release_date": formatted_release_date,
            "firmwares": []
        }

        for firmware1 in data1.get("firmwares", []):
            created_at1 = firmware1.get("created_at")
            converted_created_at1 = parse(created_at1).strftime("%Y.%m.%d")
            filtered_firmware1 = {
                "id": firmware1.get("id"),
                "version": "iOS " + firmware1.get("version") if device_name == "iPhone" else
                           "iPadOS " + firmware1.get("version") if device_name == "iPad" else
                           "MacOS " + firmware1.get("version") if device_name == "Mac" else firmware1.get("version"),
                "build_id": firmware1.get("build_id"),
                "size": firmware1.get("size"),
                "url": firmware1.get("url"),
                "created_at": converted_created_at1,
                "type": firmware1.get("type"),
                "signing": firmware1.get("signing")
            }
            filtered_data1["firmwares"].append(filtered_firmware1)

        if url2:
            response2 = requests.get(url2)
            data2 = response2.json()

            release_date_str = data2.get("release_date")
            release_date_obj = parse(release_date_str)
            formatted_release_date = release_date_obj.strftime("%Y.%m.%d")

            filtered_data2 = {
                "id": data2.get("id"),
                "updated_at": data2.get("updated_at"),
                "name": data2.get("name"),
                "identifier": data2.get("identifier"),
                "release_date": formatted_release_date,
                "firmwares": []
            }

            for firmware2 in data2.get("firmwares", []):
                created_at2 = firmware2.get("created_at")
                converted_created_at2 = parse(created_at2).strftime("%Y.%m.%d")
                filtered_firmware2 = {
                    "id": firmware2.get("id"),
                    "version": firmware2.get("version"),
                    "build_id": firmware2.get("build_id"),
                    "size": firmware2.get("size"),
                    "url": firmware2.get("url"),
                    "created_at": converted_created_at2,
                    "type": firmware2.get("type"),
                    "signing": firmware2.get("signing")
                }
                filtered_data2["firmwares"].append(filtered_firmware2)

            if filtered_data1.get("name") == filtered_data2.get("name"):
                filtered_data1["firmwares"].extend(filtered_data2["firmwares"])

        all_data.append(filtered_data1)

    # 输出为JSON格式并保存为相应设备名称的文件
    output_json = json.dumps(all_data, ensure_ascii=False)
    filename = f"{device_name}.json"
    with open(filename, "w", encoding="utf-8") as file:
        file.write(output_json)

    print(f"已保存JSON文件: {filename}")

import requests
import json
import datetime

def format_date(date_str):
    # 将日期字符串解析为datetime对象
    date = datetime.datetime.fromisoformat(date_str)

    # 将datetime对象转换为年月日格式字符串
    return date.strftime("%Y.%m.%d")

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

        filtered_data1 = {
            "id": data1.get("id"),
            "name": data1.get("name"),
            "identifier": data1.get("identifier"),
            "release_date": data1.get("release_date"),
            "firmwares": []
        }

        for firmware1 in data1.get("firmwares", []):
            filtered_firmware1 = {
                "id": firmware1.get("id"),
                "version": "iOS " + firmware1.get("version") if device_name == "iPhone" else
                           "iPadOS " + firmware1.get("version") if device_name == "iPad" else
                           "MacOS " + firmware1.get("version") if device_name == "Mac" else firmware1.get("version"),
                "build_id": firmware1.get("build_id"),
                "size": str(round(firmware1.get("size") / 1073741824, 2)) + "GB",
                "url": firmware1.get("url"),
                "created_at": firmware1.get("created_at"),
                "type": firmware1.get("type"),
                "signing": firmware1.get("signing")
            }
            filtered_data1["firmwares"].append(filtered_firmware1)

        if url2:
            response2 = requests.get(url2)
            data2 = response2.json()

            filtered_data2 = {
                "id": data2.get("id"),
                "name": data2.get("name"),
                "identifier": data2.get("identifier"),
                "release_date": data2.get("release_date"),
                "firmwares": []
            }

            for firmware2 in data2.get("firmwares", []):
                filtered_firmware2 = {
                    "id": firmware2.get("id"),
                    "version": firmware2.get("version"),
                    "build_id": firmware2.get("build_id"),
                    "size": str(round(firmware2.get("size") / 1073741824, 2)) + "GB",
                    "url": firmware2.get("url"),
                    "created_at": firmware2.get("created_at"),
                    "type": firmware2.get("type"),
                    "signing": firmware2.get("signing")
                }
                filtered_data2["firmwares"].append(filtered_firmware2)

            if filtered_data1.get("name") == filtered_data2.get("name"):
                filtered_data1["firmwares"].extend(filtered_data2["firmwares"])

        all_data.append(filtered_data1)

    # 将每个固件数据中的created_at和release_date转换为年月日格式   
    for data in all_data:
        "release_date" = format_date("release_date")
        for firmware in data["firmwares"]:
            firmware["created_at"] = format_date(firmware["created_at"])


    # 输出为JSON格式并保存为相应设备名称的文件
    output_json = json.dumps(all_data, ensure_ascii=False)
    filename = f"{device_name}.json"
    with open(filename, "w", encoding="utf-8") as file:
        file.write(output_json)

    print(f"已保存JSON文件: {filename}")

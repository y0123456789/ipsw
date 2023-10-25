import requests
import json
import datetime

def format_date(date_str):
    date = datetime.datetime.fromisoformat(date_str)
    return date.strftime("%Y.%m.%d")

devices = {
    "device1": "iPhone",
    "device2": "iPad",
    "device3": "Mac"
}

for device_key, device_name in devices.items():
    device_url = f"https://betahub.cn/api/apple/devices/{device_name}"
    response = requests.get(device_url)
    devices_data = response.json()

    firmware_data = {}  # 用于存储相同identifier的固件数据

    for device in devices_data:
        identifier = device.get("identifier")

        url1 = f"https://betahub.cn/api/apple/firmwares/{identifier}?type=1"
        url2 = f"https://betahub.cn/api/apple/firmwares/{identifier}?type=2"

        response1 = requests.get(url1)
        data1 = response1.json()

        if identifier in firmware_data:
            # 如果已经存在相同identifier的数据，将固件数据合并
            firmware_data[identifier]['firmwares'].extend(data1['firmwares'])
        else:
            firmware_data[identifier] = {
                "id": data1.get("id"),
                "name": data1.get("name"),
                "identifier": data1.get("identifier"),
                "release_date": format_date(data1.get("release_date")),
                "firmwares": data1.get("firmwares")
            }

        if url2:
            response2 = requests.get(url2)
            data2 = response2.json()

            # 同样，将相同identifier的数据合并
            firmware_data[identifier]['firmwares'].extend(data2['firmwares'])

    # 将每个固件数据中的created_at转换为年月日格式
    for identifier, data in firmware_data.items():
        for firmware in data["firmwares"]:
            firmware["created_at"] = format_date(firmware["created_at"])

    # 输出为JSON格式并保存为以identifier命名的文件
    for identifier, data in firmware_data.items():
        output_json = json.dumps(data, ensure_ascii=False)
        filename = f"{identifier}.json"
        with open(filename, "w", encoding="utf-8") as file:
            file.write(output_json)
        print(f"已保存JSON文件: {filename}")

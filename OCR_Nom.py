import requests
import json
import os
from PIL import Image
import io

upload_url = "https://tools.clc.hcmus.edu.vn/api/web/clc-sinonom/image-upload"
ocr_url = "https://tools.clc.hcmus.edu.vn/api/web/clc-sinonom/image-ocr"

headers = {
                    "User-Agent":"test 123"

        }


output_file_name = "Label.txt"


def upload_and_ocr_nom_image(image_path, output_file):
    
    with open(image_path, "rb") as image_file:
        file = {
            "image_file": image_file
        }
        upload_response = requests.post(upload_url,headers=headers, files=file)
        

        if upload_response.status_code != 200:
            print(f"Upload image failed with status code {upload_response.status_code}")
            return False

        try:
            upload_response = upload_response.json()
        except json.JSONDecodeError:
            print("Failed to decode upload response as JSON")
            return False

        if upload_response["code"] == "000000":
            # Get file_name from data field in the response
            file_name_image = upload_response["data"]["file_name"]
            print(f"Get file_name successfully: {file_name_image}")
            # Prepare data for OCR
            ocr_data = {
                "ocr_id": 1,
                "file_name":  file_name_image
            }
            ocr_headers = headers.copy()
            ocr_headers["Content-Type"] = "application/json"

            ocr_response = requests.post(ocr_url, data=json.dumps(ocr_data), headers=ocr_headers)
            try:
                ocr_response = ocr_response.json()
            except json.JSONDecodeError:
                print("Failed to decode OCR response as JSON")
                return False
           # print(f"OCR Response received: {ocr_response}")
           

            if ocr_response["code"] == "000000":
                ocr_result_file_name = ocr_response["data"]["result_file_name"]
                #print(f"OCR Result: {ocr_result_file_name}")
                with open(output_file, "a", encoding="utf-8", errors="replace") as ocr_result_file:
                    
                    result_text = f"ID: {ocr_result_file_name}\OCR Result: {ocr_response['data']['result_bbox']}\n"
                    ocr_result_file.write(result_text)
                print(f"OCR results appended to {output_file}")
                return True
            else:
                print(f"OCR failed with code: {ocr_response['code']}")
        else:
            print(f"Upload failed with code: {upload_response['code']}")
    return False

# 472 481 486 -> 495 497
def main():
    image_dir = "extracted_images"
    start_page = 370  # Customize the start page number
    end_page = 375   # Customize the end page number
    output_file = output_file_name
    with open(output_file, "w", encoding="utf-8", errors="replace") as f:
        f.write("")  # Clear the file at the start
    for page_number in range(start_page, end_page + 1):
        for image_file in os.listdir(image_dir):
            if int(image_file.split('_')[1].split('.')[0]) == page_number:
                image_path = os.path.join(image_dir, image_file)
                ocr_result = upload_and_ocr_nom_image(image_path, output_file)
                if ocr_result:
                    print(f"OCR completed for {image_file}")



if __name__ == "__main__":
    main()
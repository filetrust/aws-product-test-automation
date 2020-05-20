![](https://github.com/filetrust/aws-product-test-automation/workflows/Upload%20Python%20Package/badge.svg)

# aws-product-test-automation
A small package for testing Glasswall AWS product endpoints

## Getting Started

```cmd
pip install glasswall-aws-product-test-automation
```

### Prerequisites

* [Python >= 3.6](https://www.python.org/downloads/)

### Usage

```cmd
s93_test_automation --product "PRODUCT" --endpoint "ENDPOINT" --api_key "API_KEY"
```

### Arguments

| Argument        | Short | Necessity | Description |
| --------------- | :---: | :-------: | :- |
| --product       | -p    | Required  | *(str)* Name of a product corresponding to a directory in [s93_test_automation/integration_tests](https://github.com/filetrust/aws-product-test-automation/tree/master/s93_test_automation/integration_tests).<br>e.g. `"rebuild"` |
| --endpoint      | -e    | Required  | *(str)* API Gateway product endpoint url.<br> e.g. `"https://8oiyjy8w63.execute-api.us-west-2.amazonaws.com/Prod/api/Rebuild"` |
| --api_key       | -a    | Required  | *(str)* An AWS API key that grants access to the endpoint specified as well as other Glasswall product endpoints, such as the presigned url generator.<br>e.g. `"a612ciXevo7FM9UKlkaj2D27s6u7Nieb6K2z9929d"` |
| --test_files    | -t    | Optional  | **This functionality is currently disabled.**<br>*(str)* A directory containing external files to perform basic status code tests on. Defaults to `s93_test_automation/data/files/external`  |
| --logging_level | -l    | Optional  | *(str)* The logging level of the Python logging module. Defaults to `INFO`. Valid values are: `NOTSET`,`DEBUG`,`INFO`,`WARNING`,`ERROR`,`CRITICAL` |

### Example run (2020/05/14)
<details>
<summary>Click to expand</summary>
    
```cmd
s93_test_automation --product "rebuild" --endpoint "***" --api_key "***"

INFO:glasswall:Setting up Test_rebuild_base64
test_post___bmp_32kb___returns_status_code_200_protected_file (test_rebuild_base64.Test_rebuild_base64) ... ok
test_post___bmp_32kb_invalid_api_key___returns_status_code_403 (test_rebuild_base64.Test_rebuild_base64) ... ok
test_post___bmp_over_6mb___returns_status_code_413 (test_rebuild_base64.Test_rebuild_base64) ... skipped '6 - 10mb edge case, results in status_code 500'   
test_post___doc_embedded_images_12kb_content_management_policy_allow___returns_status_code_200_identical_file (test_rebuild_base64.Test_rebuild_base64) ... ok
test_post___doc_embedded_images_12kb_content_management_policy_disallow___returns_status_code_200_disallowed_json (test_rebuild_base64.Test_rebuild_base64) ... ok
test_post___doc_embedded_images_12kb_content_management_policy_sanitise___returns_status_code_200_sanitised_file (test_rebuild_base64.Test_rebuild_base64) ... ok
test_post___external_files___returns_200_ok_for_all_files (test_rebuild_base64.Test_rebuild_base64) ... skipped ''
test_post___jpeg_corrupt_10kb___returns_status_code_422 (test_rebuild_base64.Test_rebuild_base64) ... ok
test_post___txt_1kb___returns_status_code_422 (test_rebuild_base64.Test_rebuild_base64) ... ok
test_post___xls_malware_macro_48kb___returns_status_code_200_sanitised_file (test_rebuild_base64.Test_rebuild_base64) ... ok
INFO:glasswall:Setting up Test_rebuild_file
test_post___bmp_32kb___returns_status_code_200_protected_file (test_rebuild_file.Test_rebuild_file) ... ok
test_post___bmp_32kb_invalid_api_key___returns_status_code_403 (test_rebuild_file.Test_rebuild_file) ... ok
test_post___bmp_over_6mb___returns_status_code_413 (test_rebuild_file.Test_rebuild_file) ... skipped '6 - 10mb edge case, results in status_code 500'
test_post___doc_embedded_images_12kb_content_management_policy_allow___returns_status_code_200_identical_file (test_rebuild_file.Test_rebuild_file) ... ok
test_post___doc_embedded_images_12kb_content_management_policy_disallow___returns_status_code_200_disallowed_json (test_rebuild_file.Test_rebuild_file) ... ok
test_post___doc_embedded_images_12kb_content_management_policy_sanitise___returns_status_code_200_sanitised_file (test_rebuild_file.Test_rebuild_file) ... ok
test_post___external_files___returns_200_ok_for_all_files (test_rebuild_file.Test_rebuild_file) ... skipped ''
test_post___jpeg_corrupt_10kb___returns_status_code_422 (test_rebuild_file.Test_rebuild_file) ... ok
test_post___txt_1kb___returns_status_code_422 (test_rebuild_file.Test_rebuild_file) ... ok
test_post___xls_malware_macro_48kb___returns_status_code_200_sanitised_file (test_rebuild_file.Test_rebuild_file) ... ok
INFO:glasswall:Setting up Test_rebuild_url
INFO:glasswall:Generating presigned urls...
INFO:glasswall:File uploaded to: customer-uploaded-files/b0fd56c0-f3f1-42e1-b4d6-23133f15092e/15-05-2020 12:42:47/bmp_32kb.bmp
INFO:glasswall:File uploaded to: customer-uploaded-files/1a7447c0-7ee8-4e4d-b39d-0b18f9898ed1/15-05-2020 12:42:49/bmp_5.93mb.bmp
INFO:glasswall:File uploaded to: customer-uploaded-files/9a4c6962-032d-4e24-aef5-b50bf9acba21/15-05-2020 12:42:56/bmp_6.12mb.bmp
INFO:glasswall:File uploaded to: customer-uploaded-files/3ad4c097-6acc-49ac-8c8a-6745fc40cf65/15-05-2020 12:43:02/txt_1kb.txt
INFO:glasswall:File uploaded to: customer-uploaded-files/eabbacd6-fb0e-4af6-9e75-64283e95dbac/15-05-2020 12:43:02/doc_embedded_images_12kb.docx
INFO:glasswall:File uploaded to: customer-uploaded-files/75ccbd10-a5f4-4a46-8ef5-24143cd73af7/15-05-2020 12:43:03/CalcTest.xls
test_post___bmp_32kb___returns_status_code_200_protected_file (test_rebuild_url.Test_rebuild_url) ... ok
test_post___bmp_32kb_invalid_api_key___returns_status_code_403 (test_rebuild_url.Test_rebuild_url) ... ok
test_post___bmp_32kb_no_api_key___returns_status_code_403 (test_rebuild_url.Test_rebuild_url) ... ok
test_post___doc_embedded_images_12kb_content_management_policy_allow___returns_status_code_200_identical_file (test_rebuild_url.Test_rebuild_url) ... ok
test_post___doc_embedded_images_12kb_content_management_policy_disallow___returns_status_code_200_disallowed_json (test_rebuild_url.Test_rebuild_url) ... ok
test_post___doc_embedded_images_12kb_content_management_policy_sanitise___returns_status_code_200_sanitised_file (test_rebuild_url.Test_rebuild_url) ... ok
test_post___jpeg_corrupt_10kb___returns_status_code_422 (test_rebuild_url.Test_rebuild_url) ... skipped 'waiting for update to the presigned url lambda to allow files with no extension'
test_post___txt_1kb___returns_status_code_422 (test_rebuild_url.Test_rebuild_url) ... ok
test_post___xls_malware_macro_48kb___returns_status_code_200_sanitised_file (test_rebuild_url.Test_rebuild_url) ... ok

----------------------------------------------------------------------
Ran 29 tests in 34.634s

OK (skipped=5)
```
</details>

## Built With

* [Python 3.8.1 64-bit](https://www.python.org/downloads/release/python-381/)

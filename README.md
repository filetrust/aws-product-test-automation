![](https://github.com/filetrust/aws-product-test-automation/workflows/Upload%20Python%20Package/badge.svg)

# aws-product-test-automation
A small package for testing Glasswall AWS product endpoints

## Getting Started

For first download:

```cmd
pip install glasswall-aws-product-test-automation
```

To upgrade:

```cmd
pip install --upgrade glasswall-aws-product-test-automation
```

### Prerequisites

* [Python >= 3.6](https://www.python.org/downloads/)

### Usage

To run for a product using a jwt_token:

```cmd
s93_test_automation --product "PRODUCT" --key_type "jwt_token"  --endpoint "ENDPOINT" --api_key "API_KEY" --jwt_token "JWT_TOKEN" --invalid_token "INVALID_TOKEN"
```

To run for a product using a x_api_key:

```cmd
s93_test_automation --product "PRODUCT" --key_type "x_api_key" --endpoint "ENDPOINT" --api_key "API_KEY" --x_api_key "X_API_KEY"
```

### Arguments

| Argument         | Short | Necessity | Description |
| ---------------- | :---: | :-------: | :- |
| --product        | -p    | Required  | *(str)* Name of a product corresponding to a directory in [s93_test_automation/integration_tests](https://github.com/filetrust/aws-product-test-automation/tree/master/s93_test_automation/integration_tests).<br>e.g. `"rebuild"` |
| --endpoint       | -e    | Required  | *(str)* API Gateway product endpoint url.<br> e.g. `"https://8oiyjy8w63.execute-api.us-west-2.amazonaws.com/Prod/api/Rebuild"` |
| --key_type        | -k    | Required  | *(str)* What type of access key is being used.<br>e.g. `"x_api_key" or "jwt_token"` |
| --api_key        | -a    | Required  | *(str)* An AWS API key that grants access to the presigned url generator.<br>e.g. `"a612ciXevo7FM9UKlkaj2D27s6u7Nieb6K2z9929d"` |
| --x_api_key      | -x    | Optional  | *(str)* An AWS API key that grants access to the endpoint specified as well as other Glasswall product endpoints.<br>e.g. `"a612ciXevo7FM9UKlkaj2D27s6u7Nieb6K2z9929d"` |
| --jwt_token      | -j    | Optional  | *(str)* An authorization token that grants access to the endpoint specified.<br>e.g. `"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJPbmxpbmUgSldUIEJ1aWxkZXIiLCJpYXQiOjE1OTUwMDE3MDIsImV4cCI6..."` |
| --invalid_token  | -i    | Optional  | *(str)* An invalid version of the jwt_token that will not grant access to the endpoint specified .<br>e.g. `"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJPbmxpbmUgSldUIEJ1aWxkZXIiLCJpYXQiOjE1OTUwMDE3MDIsImV4cCI6..."` |
| --test_files     | -t    | Optional  | **This functionality is currently disabled.**<br>*(str)* A directory containing external files to perform basic status code tests on. Defaults to `s93_test_automation/data/files/external`  |
| --logging_level  | -l    | Optional  | *(str)* The logging level of the Python logging module. Defaults to `INFO`. Valid values are: `NOTSET`,`DEBUG`,`INFO`,`WARNING`,`ERROR`,`CRITICAL` |

### Example run (2020/07/17)

<details>
<summary>Click to expand</summary>

```cmd
s93_test_automation --product "rebuild" --key_type "x_api_key" --endpoint "***" --api_key "***" --x_api_key "***"
INFO:glasswall:Setting up Test_rebuild_base64
test_post___bmp_32kb___returns_status_code_200_protected_file (test_rebuild_xapi_base64.Test_rebuild_base64)
1Test_File submit using base64 code & less than 6mb with valid x-api key is successful ... ok
test_post___bmp_32kb_invalid_api_key___returns_status_code_403 (test_rebuild_xapi_base64.Test_rebuild_base64)
3-Test_File submit using base64 code & less than 6mb with invalid x-api key is unsuccessful ... ok
test_post___bmp_over_6mb___returns_status_code_413 (test_rebuild_xapi_base64.Test_rebuild_base64)
2-Test_Accurate error returned for a over 6mb file submit using base64 code with valid x-api key ... skipped '6 - 10mb edge case, results in status_code 500'
test_post___doc_embedded_images_12kb_content_management_policy_allow___returns_status_code_200_identical_file (test_rebuild_xapi_base64.Test_rebuild_base64)
4-Test_The default cmp policy is applied to submitted file using base64 code ... ok
test_post___doc_embedded_images_12kb_content_management_policy_disallow___returns_status_code_200_disallowed_json (test_rebuild_xapi_base64.Test_rebuild_base64)
4-Test_The default cmp policy is applied to submitted file using base64 code ... ok
test_post___doc_embedded_images_12kb_content_management_policy_sanitise___returns_status_code_200_sanitised_file (test_rebuild_xapi_base64.Test_rebuild_base64)
4-Test_The default cmp policy is applied to submitted file using base64 code ... ok
test_post___external_files___returns_200_ok_for_all_files (test_rebuild_xapi_base64.Test_rebuild_base64) ... skipped ''
test_post___jpeg_corrupt_10kb___returns_status_code_422 (test_rebuild_xapi_base64.Test_rebuild_base64)
12-Test_upload of files with issues and or malware using base64 code with valid x-api key ... ok
test_post___txt_1kb___returns_status_code_422 (test_rebuild_xapi_base64.Test_rebuild_base64)
10-Test_unsupported file upload using base64 code & less than 6mb with valid x-api key is unsuccessful ... ok
test_post___xls_malware_macro_48kb___returns_status_code_200_sanitised_file (test_rebuild_xapi_base64.Test_rebuild_base64)
12-Test_upload of files with issues and or malware using base64 code with valid x-api key ... ok
INFO:glasswall:Setting up Test_rebuild_file
test_post___bmp_32kb___returns_status_code_200_protected_file (test_rebuild_xapi_file.Test_rebuild_file)
1Test_File submit using file endpoint & less than 6mb with valid x-api key is successful ... ok
test_post___bmp_32kb_invalid_x_api_key___returns_status_code_403 (test_rebuild_xapi_file.Test_rebuild_file)
3-Test_File submit using file endpoint & less than 6mb with invalid x-api key is unsuccessful ... ok
test_post___bmp_over_6mb___returns_status_code_413 (test_rebuild_xapi_file.Test_rebuild_file)
2-Test_Accurate error returned for a over 6mb file submit using file endpoint with valid x-api key ... skipped '6 - 10mb edge case, results in status_code 500'
test_post___doc_embedded_images_12kb_content_management_policy_allow___returns_status_code_200_identical_file (test_rebuild_xapi_file.Test_rebuild_file)
4-Test_The default cmp policy is applied to submitted file using file endpoint ... ok
test_post___doc_embedded_images_12kb_content_management_policy_disallow___returns_status_code_200_disallowed_json (test_rebuild_xapi_file.Test_rebuild_file)
4-Test_The default cmp policy is applied to submitted file using file endpoint ... ok
test_post___doc_embedded_images_12kb_content_management_policy_sanitise___returns_status_code_200_sanitised_file (test_rebuild_xapi_file.Test_rebuild_file)
4-Test_The default cmp policy is applied to submitted file using file endpoint ... ok
test_post___external_files___returns_200_ok_for_all_files (test_rebuild_xapi_file.Test_rebuild_file) ... skipped ''
test_post___jpeg_corrupt_10kb___returns_status_code_422 (test_rebuild_xapi_file.Test_rebuild_file)
12-Test_upload of files with issues and or malware using file endpoint with valid x-api key ... ok
test_post___txt_1kb___returns_status_code_422 (test_rebuild_xapi_file.Test_rebuild_file)
10-Test_unsupported file upload using file endpoint & less than 6mb with valid x-api key is unsuccessful ... ok
test_post___xls_malware_macro_48kb___returns_status_code_200_sanitised_file (test_rebuild_xapi_file.Test_rebuild_file)
12-Test_upload of files with issues and or malware using file endpoint with valid x-api key ... ok
INFO:glasswall:Setting up Test_rebuild_url
INFO:glasswall:Generating presigned urls...
INFO:glasswall:File uploaded to: customer-uploaded-files/b1d9261c-06c1-41e1-9290-8111decd60a2/17-07-2020 05:04:46/bmp_32kb.bmp
INFO:glasswall:File uploaded to: customer-uploaded-files/6fc09b7a-c613-48c3-b8c7-8658da349c5a/17-07-2020 05:04:49/bmp_5.93mb.bmp
INFO:glasswall:File uploaded to: customer-uploaded-files/8834a213-54a8-45db-87bc-0b62b9d10c03/17-07-2020 05:04:50/bmp_6.12mb.bmp
INFO:glasswall:File uploaded to: customer-uploaded-files/b70670c1-1481-48b3-900e-6b6d4d267817/17-07-2020 05:04:51/txt_1kb.txt
INFO:glasswall:File uploaded to: customer-uploaded-files/7e6d42e1-379f-4b75-94af-ad3744418eb7/17-07-2020 05:04:51/doc_embedded_images_12kb.docx
INFO:glasswall:File uploaded to: customer-uploaded-files/07c1dd4b-f7df-4bcf-adae-57ea18b01cb5/17-07-2020 05:04:51/CalcTest.xls
test_post___bmp_32kb___returns_status_code_200_protected_file (test_rebuild_xapi_url.Test_rebuild_url)
5-Test_File submit using pre-signed url with valid x-api key is successful ... ok
test_post___bmp_32kb_invalid_api_key___returns_status_code_403 (test_rebuild_xapi_url.Test_rebuild_url)
6b-Test_File submit using pre-signed url with invalid x-api key is unsuccessful ... ok
test_post___bmp_32kb_no_api_key___returns_status_code_403 (test_rebuild_xapi_url.Test_rebuild_url)
6a-Test_File submit using pre-signed url with no x-api key is unsuccessful ... ok
test_post___doc_embedded_images_12kb_content_management_policy_allow___returns_status_code_200_identical_file (test_rebuild_xapi_url.Test_rebuild_url)
7a-Test_The default cmp policy is applied to submitted file using pre-signed url ... ok
test_post___doc_embedded_images_12kb_content_management_policy_disallow___returns_status_code_200_disallowed_json (test_rebuild_xapi_url.Test_rebuild_url)
7c-Test_The default cmp policy is applied to submitted file using pre-signed url ... ok
test_post___doc_embedded_images_12kb_content_management_policy_sanitise___returns_status_code_200_sanitised_file (test_rebuild_xapi_url.Test_rebuild_url)
7b-Test_The default cmp policy is applied to submitted file using pre-signed url ... ok
test_post___jpeg_corrupt_10kb___returns_status_code_422 (test_rebuild_xapi_url.Test_rebuild_url)
11b-Test_upload of files with issues and or malware using presigned with valid x-api key ... skipped 'waiting for update to the presigned url lambda to allow files with no extension'
test_post___txt_1kb___returns_status_code_422 (test_rebuild_xapi_url.Test_rebuild_url)
9-Test_unsupported file upload using pre-signed url with valid x-api key is unsuccessful ... ok
test_post___xls_malware_macro_48kb___returns_status_code_200_sanitised_file (test_rebuild_xapi_url.Test_rebuild_url)
11a-Test_upload of files with issues and or malware using presigned with valid x-api key ... ok

----------------------------------------------------------------------
Ran 29 tests in 11.399s

OK (skipped=5)



s93_test_automation --product "rebuild" --key_type "jwt_token" --endpoint "***" --api_key "***" --jwt_token "***" --invalid_token "***"
INFO:glasswall:Setting up Test_rebuild_base64
test_post___bmp_32kb___returns_status_code_200_protected_file (test_rebuild_jwt_base64.Test_rebuild_base64)
1Test_File submit using base64 code & less than 6mb with valid jwt token is successful ... ok
test_post___bmp_32kb_invalid_token___returns_status_code_403 (test_rebuild_jwt_base64.Test_rebuild_base64)
3-Test_File submit using base64 code & less than 6mb with invalid jwt token is unsuccessful ... ok
test_post___bmp_over_6mb___returns_status_code_413 (test_rebuild_jwt_base64.Test_rebuild_base64)
2-Test_Accurate error returned for a over 6mb file submit using base64 code with valid jwt token ... skipped '6 - 10mb edge case, results in status_code 500'
test_post___doc_embedded_images_12kb_content_management_policy_allow___returns_status_code_200_identical_file (test_rebuild_jwt_base64.Test_rebuild_base64)
4-Test_The default cmp policy is applied to submitted file using base64 code ... ok
test_post___doc_embedded_images_12kb_content_management_policy_disallow___returns_status_code_200_disallowed_json (test_rebuild_jwt_base64.Test_rebuild_base64)
4-Test_The default cmp policy is applied to submitted file using base64 code ... ok
test_post___doc_embedded_images_12kb_content_management_policy_sanitise___returns_status_code_200_sanitised_file (test_rebuild_jwt_base64.Test_rebuild_base64)
4-Test_The default cmp policy is applied to submitted file using base64 code ... ok
test_post___external_files___returns_200_ok_for_all_files (test_rebuild_jwt_base64.Test_rebuild_base64) ... skipped ''
test_post___jpeg_corrupt_10kb___returns_status_code_422 (test_rebuild_jwt_base64.Test_rebuild_base64)
12-Test_upload of files with issues and or malware using base64 code with valid jwt token ... ok
test_post___txt_1kb___returns_status_code_422 (test_rebuild_jwt_base64.Test_rebuild_base64)
10-Test_unsupported file upload using base64 code & less than 6mb with valid jwt token is unsuccessful ... ok
test_post___xls_malware_macro_48kb___returns_status_code_200_sanitised_file (test_rebuild_jwt_base64.Test_rebuild_base64)
12-Test_upload of files with issues and or malware using base64 code with valid jwt token ... ok
INFO:glasswall:Setting up Test_rebuild_file
test_post___bmp_32kb___returns_status_code_200_protected_file (test_rebuild_jwt_file.Test_rebuild_file)
1Test_File submit using file endpoint & less than 6mb with valid jwt token is successful ... ok
test_post___bmp_32kb_invalid_token___returns_status_code_403 (test_rebuild_jwt_file.Test_rebuild_file)
3-Test_File submit using file endpoint & less than 6mb with invalid token is unsuccessful ... ok
test_post___bmp_over_6mb___returns_status_code_413 (test_rebuild_jwt_file.Test_rebuild_file)
2-Test_Accurate error returned for a over 6mb file submit using file endpoint with valid jwt token ... skipped '6 - 10mb edge case, results in status_code 500'
test_post___doc_embedded_images_12kb_content_management_policy_allow___returns_status_code_200_identical_file (test_rebuild_jwt_file.Test_rebuild_file)
4-Test_The default cmp policy is applied to submitted file using file endpoint ... ok
test_post___doc_embedded_images_12kb_content_management_policy_disallow___returns_status_code_200_disallowed_json (test_rebuild_jwt_file.Test_rebuild_file)
4-Test_The default cmp policy is applied to submitted file using file endpoint ... ok
test_post___doc_embedded_images_12kb_content_management_policy_sanitise___returns_status_code_200_sanitised_file (test_rebuild_jwt_file.Test_rebuild_file)
4-Test_The default cmp policy is applied to submitted file using file endpoint ... ok
test_post___external_files___returns_200_ok_for_all_files (test_rebuild_jwt_file.Test_rebuild_file) ... skipped ''
test_post___jpeg_corrupt_10kb___returns_status_code_422 (test_rebuild_jwt_file.Test_rebuild_file)
12-Test_upload of files with issues and or malware using file endpoint with valid jwt token ... ok
test_post___txt_1kb___returns_status_code_422 (test_rebuild_jwt_file.Test_rebuild_file)
10-Test_unsupported file upload using file endpoint & less than 6mb with valid jwt token is unsuccessful ... ok
test_post___xls_malware_macro_48kb___returns_status_code_200_sanitised_file (test_rebuild_jwt_file.Test_rebuild_file)
12-Test_upload of files with issues and or malware using file endpoint with valid jwt token ... ok
INFO:glasswall:Setting up Test_rebuild_url
INFO:glasswall:Generating presigned urls...
INFO:glasswall:File uploaded to: customer-uploaded-files/ef394621-5904-45ff-b20a-c8f531fd6711/17-07-2020 05:07:14/bmp_32kb.bmp
INFO:glasswall:File uploaded to: customer-uploaded-files/2bddfa9f-fbeb-4f2e-bb77-1fa38cc18947/17-07-2020 05:07:14/bmp_5.93mb.bmp
INFO:glasswall:File uploaded to: customer-uploaded-files/9bc2bc11-b09c-4cd0-aed3-149350f0858a/17-07-2020 05:07:16/bmp_6.12mb.bmp
INFO:glasswall:File uploaded to: customer-uploaded-files/5da1f694-a6d3-4499-961c-29ab0e35b177/17-07-2020 05:07:17/txt_1kb.txt
INFO:glasswall:File uploaded to: customer-uploaded-files/1c94b1bb-bb49-4fdf-b79c-efbbfbc0a4e0/17-07-2020 05:07:17/doc_embedded_images_12kb.docx
INFO:glasswall:File uploaded to: customer-uploaded-files/73c69a0c-057d-41a5-ad9b-078fc65d1426/17-07-2020 05:07:17/CalcTest.xls
test_post___bmp_32kb___returns_status_code_200_protected_file (test_rebuild_jwt_url.Test_rebuild_url)
5-Test_File submit using pre-signed url with valid jwt token is successful ... ok
test_post___bmp_32kb_invalid_token___returns_status_code_403 (test_rebuild_jwt_url.Test_rebuild_url)
6b-Test_File submit using pre-signed url with invalid token is unsuccessful ... ok
test_post___bmp_32kb_no_jwt_token___returns_status_code_403 (test_rebuild_jwt_url.Test_rebuild_url)
6a-Test_File submit using pre-signed url with no jwt token is unsuccessful ... ok
test_post___doc_embedded_images_12kb_content_management_policy_allow___returns_status_code_200_identical_file (test_rebuild_jwt_url.Test_rebuild_url)
7a-Test_The default cmp policy is applied to submitted file using pre-signed url ... ok
test_post___doc_embedded_images_12kb_content_management_policy_disallow___returns_status_code_200_disallowed_json (test_rebuild_jwt_url.Test_rebuild_url)
7c-Test_The default cmp policy is applied to submitted file using pre-signed url ... ok
test_post___doc_embedded_images_12kb_content_management_policy_sanitise___returns_status_code_200_sanitised_file (test_rebuild_jwt_url.Test_rebuild_url)
7b-Test_The default cmp policy is applied to submitted file using pre-signed url ... ok
test_post___jpeg_corrupt_10kb___returns_status_code_422 (test_rebuild_jwt_url.Test_rebuild_url)
11b-Test_upload of files with issues and or malware using presigned with valid jwt token ... skipped 'waiting for update to the presigned url lambda to allow files with no extension'
test_post___txt_1kb___returns_status_code_422 (test_rebuild_jwt_url.Test_rebuild_url)
9-Test_unsupported file upload using pre-signed url with valid jwt token is unsuccessful ... ok
test_post___xls_malware_macro_48kb___returns_status_code_200_sanitised_file (test_rebuild_jwt_url.Test_rebuild_url)
11a-Test_upload of files with issues and or malware using presigned with valid jwt token ... ok

----------------------------------------------------------------------
Ran 29 tests in 12.822s

OK (skipped=5)
```
</details>

## Built With

* [Python 3.8.1 64-bit](https://www.python.org/downloads/release/python-381/)

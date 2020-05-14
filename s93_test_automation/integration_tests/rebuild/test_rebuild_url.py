

import ast
from http import HTTPStatus
import logging
log = logging.getLogger("glasswall")
import os
import requests
from s93_test_automation import _ROOT
from s93_test_automation.common import list_file_paths, get_md5, get_presigned_urls
import unittest


class Test_rebuild_url(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        log.info(f"Setting up {cls.__name__}")
        cls.endpoint                        = f"{os.environ['endpoint']}"
        cls.api_key                         = os.environ["api_key"]

        cls.endpoint_upload                 = "https://l76geea2l9.execute-api.eu-west-2.amazonaws.com/development/generate-post-presigned-url"
        cls.endpoint_download               = "https://l76geea2l9.execute-api.eu-west-2.amazonaws.com/development/generate-presigned-url"

        log.info("Generating presigned urls...")

        cls.bmp_32kb                        = os.path.join(_ROOT, "data", "files", "under_6mb", "bmp", "bmp_32kb.bmp")
        cls.bmp_32kb_urls                   = get_presigned_urls(cls.bmp_32kb, cls.endpoint_upload, cls.endpoint_download, cls.api_key)
        cls.bmp_under_6mb                   = os.path.join(_ROOT, "data", "files", "under_6mb", "bmp", "bmp_5.93mb.bmp")
        cls.bmp_under_6mb_urls              = get_presigned_urls(cls.bmp_under_6mb, cls.endpoint_upload, cls.endpoint_download, cls.api_key)
        cls.bmp_over_6mb                    = os.path.join(_ROOT, "data", "files", "over_6mb", "bmp", "bmp_6.12mb.bmp")
        cls.bmp_over_6mb_urls               = get_presigned_urls(cls.bmp_over_6mb, cls.endpoint_upload, cls.endpoint_download, cls.api_key)

        cls.txt_1kb                         = os.path.join(_ROOT, "data", "files", "under_6mb", "txt", "txt_1kb.txt")
        cls.txt_1kb_urls                    = get_presigned_urls(cls.txt_1kb, cls.endpoint_upload, cls.endpoint_download, cls.api_key)

        cls.doc_embedded_images_12kb        = os.path.join(_ROOT, "data", "files", "under_6mb", "doc", "doc_embedded_images_12kb.docx")
        cls.doc_embedded_images_12kb_urls   = get_presigned_urls(cls.doc_embedded_images_12kb, cls.endpoint_upload, cls.endpoint_download, cls.api_key)

        cls.xls_malware_macro_48kb          = os.path.join(_ROOT, "data", "files", "under_6mb", "harmless_macro", "xls", "CalcTest.xls")
        cls.xls_malware_macro_48kb_urls     = get_presigned_urls(cls.xls_malware_macro_48kb, cls.endpoint_upload, cls.endpoint_download, cls.api_key)

        # # waiting for update to the presigned url lambda to allow files with no extension
        # cls.jpeg_corrupt_10kb               = os.path.join(_ROOT, "data", "files", "under_6mb", "corrupt", "Corrupted_jpeg_png_mag_no")
        # cls.jpeg_corrupt_10kb_urls          = get_presigned_urls(cls.jpeg_corrupt_10kb, cls.endpoint_upload, cls.endpoint_download, cls.api_key)

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_post___bmp_32kb___returns_status_code_200_protected_file(self):
        """
        5-Test_File submit using pre-signed url with valid x-api key is successful
        Steps:
            Post a file payload request with file url to endpoint: '[API GATEWAY URL]/api/Rebuild' with valid x-api key
        Expected:
            The response is returned with the processed file and success code 200
        """
        # Send post request
        response = requests.post(
            url=self.endpoint,
            json={
                "InputGetUrl": self.bmp_32kb_urls.get("InputGetUrl"),
                "OutputPutUrl": self.bmp_32kb_urls.get("OutputPutUrl"),
            },
            headers={
                "x-api-key": self.api_key,
            }
        )

        # Status code should be 200, ok
        self.assertEqual(
            response.status_code,
            HTTPStatus.OK
        )

        # Response etag should be the same as the md5 of the input file
        self.assertEqual(
            ast.literal_eval(response.headers.get("gw-put-file-etag")),
            get_md5(self.bmp_32kb)
        )

    def test_post___bmp_32kb_no_api_key___returns_status_code_403(self):
        """
        6a-Test_File submit using pre-signed url with no x-api key is unsuccessful
        Steps:
            Post a file payload request with file url: '[API GATEWAY URL]/api/Rebuild/sas' with invalid x-api key
        Expected:
            The response message 'forbidden' is returned with error code '403'
        """
        # Send post request
        response = requests.post(
            url=self.endpoint,
            json={
                "InputGetUrl": self.bmp_32kb_urls.get("InputGetUrl"),
                "OutputPutUrl": self.bmp_32kb_urls.get("OutputPutUrl"),
            }
        )

        # Status code should be 403, forbidden
        self.assertEqual(
            response.status_code,
            HTTPStatus.FORBIDDEN
        )

    def test_post___bmp_32kb_invalid_api_key___returns_status_code_403(self):
        """
        6b-Test_File submit using pre-signed url with invalid x-api key is unsuccessful
        Steps:
                Post a file payload request with file url: '[API GATEWAY URL]/api/Rebuild/sas' with invalid x-api key
        Expected:
            The response message 'forbidden' is returned with error code '403'
        """
        # Send post request
        response = requests.post(
            url=self.endpoint,
            json={
                "InputGetUrl": self.bmp_32kb_urls.get("InputGetUrl"),
                "OutputPutUrl": self.bmp_32kb_urls.get("OutputPutUrl"),
            },
            headers={
                "x-api-key": self.api_key + "abcdef",
            }
        )

        # Status code should be 403, forbidden
        self.assertEqual(
            response.status_code,
            HTTPStatus.FORBIDDEN
        )

    def test_post___doc_embedded_images_12kb_content_management_policy_allow___returns_status_code_200_identical_file(self):
        """
        7a-Test_The default cmp policy is applied to submitted file using pre-signed url
        Steps:
                Set cmp policy for file type as 'cmptype'
                Post a file payload request with file url: '[API GATEWAY URL]/api/Rebuild/sas' with valid x-api key
        Expected:
        The response is returned with error code '200'
                If cmpType is 'Sanitise', Then the file is returned sanitised
                If cmpType is 'Allow', Then the file is allowed & the original file is returned
                If cmpType is 'Disallow', Then the file is allowed & the original file is returned
        """
        # Send post request
        response = requests.post(
            url=self.endpoint,
            json={
                "InputGetUrl": self.doc_embedded_images_12kb_urls.get("InputGetUrl"),
                "OutputPutUrl": self.doc_embedded_images_12kb_urls.get("OutputPutUrl"),
                "ContentManagementFlags": {
                    "PdfContentManagement": {
                        "Metadata": 0,
                        "InternalHyperlinks": 0,
                        "ExternalHyperlinks": 0,
                        "EmbeddedFiles": 0,
                        "EmbeddedImages": 0,
                        "Javascript": 0,
                        "Acroform": 0,
                        "ActionsAll": 0
                    },
                    "ExcelContentManagement": {
                        "Metadata": 0,
                        "InternalHyperlinks": 0,
                        "ExternalHyperlinks": 0,
                        "EmbeddedFiles": 0,
                        "EmbeddedImages": 0,
                        "DynamicDataExchange": 0,
                        "Macros": 0,
                        "ReviewComments": 0
                    },
                    "PowerPointContentManagement": {
                        "Metadata": 0,
                        "InternalHyperlinks": 0,
                        "ExternalHyperlinks": 0,
                        "EmbeddedFiles": 0,
                        "EmbeddedImages": 0,
                        "Macros": 0,
                        "ReviewComments": 0
                    },
                    "WordContentManagement": {
                        "Metadata": 0,
                        "InternalHyperlinks": 0,
                        "ExternalHyperlinks": 0,
                        "EmbeddedFiles": 0,
                        "EmbeddedImages": 0,
                        "DynamicDataExchange": 0,
                        "Macros": 0,
                        "ReviewComments": 0
                    }
                }
            },
            headers={
                "x-api-key": self.api_key,
            }
        )

        # Status code should be 200, ok
        self.assertEqual(
            response.status_code,
            HTTPStatus.OK
        )

        # Response etag should be the same as the md5 of the input file
        self.assertEqual(
            ast.literal_eval(response.headers.get("gw-put-file-etag")),
            get_md5(self.doc_embedded_images_12kb)
        )

    def test_post___doc_embedded_images_12kb_content_management_policy_sanitise___returns_status_code_200_sanitised_file(self):
        """
        7b-Test_The default cmp policy is applied to submitted file using pre-signed url
        Steps:
                Set cmp policy for file type as 'cmptype'
                Post a file payload request with file url: '[API GATEWAY URL]/api/Rebuild/sas' with valid x-api key
        Expected:
        The response is returned with error code '200'
                If cmpType is 'Sanitise', Then the file is returned sanitised
                If cmpType is 'Allow', Then the file is allowed & the original file is returned
                If cmpType is 'Disallow', Then the file is allowed & the original file is returned
        """
        # Send post request
        response = requests.post(
            url=self.endpoint,
            json={
                "InputGetUrl": self.doc_embedded_images_12kb_urls.get("InputGetUrl"),
                "OutputPutUrl": self.doc_embedded_images_12kb_urls.get("OutputPutUrl"),
                "ContentManagementFlags": {
                    "WordContentManagement": {
                        "Metadata": 1,
                        "InternalHyperlinks": 1,
                        "ExternalHyperlinks": 1,
                        "EmbeddedFiles": 1,
                        "EmbeddedImages": 1,
                        "DynamicDataExchange": 1,
                        "Macros": 1,
                        "ReviewComments": 1,
                    },
                },
            },
            headers={
                "x-api-key": self.api_key,
            }
        )

        # Status code should be 200, ok
        self.assertEqual(
            response.status_code,
            HTTPStatus.OK
        )

        # Response etag should be different to the md5 of the input file
        self.assertNotEqual(
            ast.literal_eval(response.headers.get("gw-put-file-etag")),
            get_md5(self.doc_embedded_images_12kb)
        )

        # etag should match expected md5
        self.assertEqual(
            ast.literal_eval(response.headers.get("gw-put-file-etag")),
            "665f3d263d7fe25b7491cbeec657abb0"
        )

    def test_post___doc_embedded_images_12kb_content_management_policy_disallow___returns_status_code_200_disallowed_json(self):
        """
        7c-Test_The default cmp policy is applied to submitted file using pre-signed url
        Steps:
            Set cmp policy for file type as 'cmptype'
            Post a file payload request with file url: '[API GATEWAY URL]/api/Rebuild/sas' with valid x-api key
        Expected:
            The response is returned with error code '200'
                If cmpType is 'Sanitise', Then the file is returned sanitised
                If cmpType is 'Allow', Then the file is allowed & the original file is returned
                If cmpType is 'Disallow', Then the file is allowed & the original file is returned
        """
        # Send post request
        response = requests.post(
            url=self.endpoint,
            json={
                "InputGetUrl": self.doc_embedded_images_12kb_urls.get("InputGetUrl"),
                "OutputPutUrl": self.doc_embedded_images_12kb_urls.get("OutputPutUrl"),
                "ContentManagementFlags": {
                    "WordContentManagement": {
                        "EmbeddedImages": 2,
                    },
                },
            },
            headers={
                "x-api-key": self.api_key,
            }
        )

        # Status code should be 200, ok
        self.assertEqual(
            response.status_code,
            HTTPStatus.OK
        )

        # JSON should have an errorMessage key
        self.assertTrue("errorMessage" in response.json().keys())

        # JSON should have isDisallowed key with value True
        self.assertTrue(response.json().get("isDisallowed"))

    def test_post___txt_1kb___returns_status_code_422(self):
        """
        9-Test_unsupported file upload using pre-signed url with valid x-api key is unsuccessful
        Execution Steps:
                Post a payload request with file url: '[API GATEWAY URL]/api/Rebuild/sas' with valid x-api key
        Expected Results:
            The response message 'Unprocessable Entity' is returned with error code '422'
        """
        # Send post request
        response = requests.post(
            url=self.endpoint,
            json={
                "InputGetUrl": self.txt_1kb_urls.get("InputGetUrl"),
                "OutputPutUrl": self.txt_1kb_urls.get("OutputPutUrl"),
            },
            headers={
                "x-api-key": self.api_key,
            }
        )

        # Status code should be 422, Unprocessable Entity
        self.assertEqual(
            response.status_code,
            HTTPStatus.UNPROCESSABLE_ENTITY
        )

    def test_post___xls_malware_macro_48kb___returns_status_code_200_sanitised_file(self):
        """
        11a-Test_upload of files with issues and or malware using presigned with valid x-api key
        Execution Steps:
            Post a payload request with file containing malware to url: '[API GATEWAY URL]/api/Rebuild/sas' with valid x-api key
            Post a payload request with file containing structural issues to url: '[API GATEWAY URL]/api/Rebuild/sas' with valid x-api key
            Post a payload request with file containing issues and malware to url: '[API GATEWAY URL]/api/Rebuild/sas' with valid x-api key
        Expected Results:
            The response message returned for file containing malware is:'OK' with success code '200'
            The response message returned for file containing structural issues is: 'Unprocessable Entity' with error code '422'
            The response message returned for file containing malware is: 'Unprocessable Entity' with error code '422'
        """
        # Send post request
        response = requests.post(
            url=self.endpoint,
            json={
                "InputGetUrl": self.xls_malware_macro_48kb_urls.get("InputGetUrl"),
                "OutputPutUrl": self.xls_malware_macro_48kb_urls.get("OutputPutUrl"),
            },
            headers={
                "x-api-key": self.api_key
            }
        )

        # Status code should be 200, ok
        self.assertEqual(
            response.status_code,
            HTTPStatus.OK
        )

        # Response etag should be different to the md5 of the input file
        self.assertNotEqual(
            ast.literal_eval(response.headers.get("gw-put-file-etag")),
            get_md5(self.xls_malware_macro_48kb)
        )

        # etag should match expected md5
        self.assertEqual(
            ast.literal_eval(response.headers.get("gw-put-file-etag")),
            "4b6ef99d2932fd735a4eed1c1ca236ee"
        )

    @unittest.skip("waiting for update to the presigned url lambda to allow files with no extension")
    def test_post___jpeg_corrupt_10kb___returns_status_code_422(self):
        """
        11b-Test_upload of files with issues and or malware using presigned with valid x-api key
        Execution Steps:
            Post a payload request with file containing malware to url: '[API GATEWAY URL]/api/Rebuild/sas' with valid x-api key
            Post a payload request with file containing structural issues to url: '[API GATEWAY URL]/api/Rebuild/sas' with valid x-api key
            Post a payload request with file containing issues and malware to url: '[API GATEWAY URL]/api/Rebuild/sas' with valid x-api key
        Expected Results:
            The response message returned for file containing malware is:'OK' with success code '200'
            The response message returned for file containing structural issues is: 'Unprocessable Entity' with error code '422'
            The response message returned for file containing malware is: 'Unprocessable Entity' with error code '422'
        """
        # Send post request
        response = requests.post(
            url=self.endpoint,
            json={
                "InputGetUrl": self.jpeg_corrupt_10kb_urls.get("InputGetUrl"),
                "OutputPutUrl": self.jpeg_corrupt_10kb_urls.get("OutputPutUrl"),
            },
            headers={
                "x-api-key": self.api_key,
            }
        )

        # Status code should be 422, Unprocessable Entity
        self.assertEqual(
            response.status_code,
            HTTPStatus.UNPROCESSABLE_ENTITY
        )


if __name__ == "__main__":
    unittest.main()



from s93_test_automation.common import get_file_bytes, list_file_paths
from base64 import b64encode, b64decode
from http import HTTPStatus
import os
import requests
from s93_test_automation import _ROOT
import unittest


class Test_rebuild_base64(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.endpoint        = f"{os.environ['endpoint']}/base64"
        cls.api_key         = os.environ["api_key"]

        cls.bmp_32kb        = os.path.join(_ROOT, "data", "files", "under_6mb", "bmp", "bmp_32kb.bmp")
        cls.bmp_under_6mb   = os.path.join(_ROOT, "data", "files", "under_6mb", "bmp", "bmp_5.93mb.bmp")
        cls.bmp_over_6mb    = os.path.join(_ROOT, "data", "files", "over_6mb", "bmp", "bmp_6.12mb.bmp")

        cls.txt_1kb         = os.path.join(_ROOT, "data", "files", "under_6mb", "txt", "txt_1kb.txt")

        cls.doc_14kb_embedded_images    = os.path.join(_ROOT, "data", "files", "under_6mb", "doc", "embedded_image_14kb.docx")

        cls.xls_48kb_malware_macro      = os.path.join(_ROOT, "data", "files", "under_6mb", "malware", "xls", "CalcTest.xls")
        cls.jpeg_corrupt_10kb           = os.path.join(_ROOT, "data", "files", "under_6mb", "corrupt", "Corrupted_jpeg_png_mag_no")

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass
    
    @unittest.skip
    def test_post___external_files___returns_200_ok_for_all_files(self):
        # Check that the directory containing test files is not empty
        external_files = list_file_paths(os.environ["test_files"])
        if external_files == []:
            return unittest.skip("No external files found.")

        for file_path in external_files:
            # Set variable for file to test
            test_file = get_file_bytes(file_path)

            # Send post request
            response = requests.post(
                url=self.endpoint,
                json={
                    "Base64": b64encode(test_file).decode()
                },
                headers={
                    "Content-Type": "application/json",
                    "x-api-key": self.api_key
                }
            )

            # Status code should be 200, ok
            self.assertEqual(
                response.status_code,
                HTTPStatus.OK
            )

    def test_post___bmp_32kb___returns_status_code_200_and_protected_file(self):
        """
        1Test_File submit using base64 code & less than 6mb with valid x-api key is successful
        Steps:
            Post file payload request to endpoint: '[API GATEWAY URL]/api/Rebuild/base64' with valid x-api key
        Expected:
        The response is returned with the processed file & success code 200
        """

        # Set variable for file to test
        test_file = get_file_bytes(self.bmp_32kb)

        # Send post request
        response = requests.post(
            url=self.endpoint,
            json={
                "Base64": b64encode(test_file).decode()
            },
            headers={
                "Content-Type": "application/json",
                "x-api-key": self.api_key
            }
        )

        # Status code should be 200, ok
        self.assertEqual(
            response.status_code,
            HTTPStatus.OK
        )

        # Response content should be identical to the test file input
        self.assertEqual(
            b64decode(response.content),
            test_file
        )

    @unittest.skip
    def test_post___bmp_over_6mb___returns_status_code_413(self):
        """
        2-Test_Accurate error returned for a over 6mb file submit using base64 code with valid x-api key
        Steps:
            Post file over 6mb payload request to endpoint: '[API GATEWAY URL]/api/Rebuild/base64' with valid x-api key
        Expected:
        The response message '' is returned with error code 400
        """

        # Set variable for file to test
        test_file = get_file_bytes(self.bmp_over_6mb)

        # Send post request
        response = requests.post(
            url=self.endpoint,
            json={
                "Base64": b64encode(test_file).decode()
            },
            headers={
                "Content-Type": "application/json",
                "x-api-key": self.api_key
            }
        )

        # Status code should be 413, Payload Too Large
        self.assertEqual(
            response.status_code,
            HTTPStatus.REQUEST_ENTITY_TOO_LARGE
        )

    def test_post___bmp_32kb_invalid_api_key___returns_status_code_403(self):
        """
        3-Test_File submit using base64 code & less than 6mb with invalid x-api key is unsuccessful
        Steps:
            Post file payload request to endpoint: '[API GATEWAY URL]/api/Rebuild/base64' with invalid x-api key
        Expected:
        return error code 401
        """

        # Set variable for file to test
        test_file = get_file_bytes(self.bmp_32kb)

        # Send post request
        response = requests.post(
            url=self.endpoint,
            json={
                "Base64": b64encode(test_file).decode()
            },
            headers={
                "Content-Type": "application/json",
                "x-api-key": ""
            }
        )

        # Status code should be 400, bad request
        self.assertEqual(
            response.status_code,
            HTTPStatus.FORBIDDEN
        )

    def test_post___bmp_32kb_content_management_policy_allow___returns_protected_file(self):
        """
        4-Test_The default cmp policy is applied to submitted file using base64 code
        Steps:
            Set cmp policy for file type as 'cmptype'
            Post file payload request to endpoint: '[API GATEWAY URL]/api/Rebuild/base64' with valid x-api key
        Expected:
        The response is returned with success code '200'
            0) If cmpType is 'Allow', Then the file is allowed & the original file is returned
            1) If cmpType is 'Sanitise', Then the file is returned sanitised
            2) If cmpType is 'Disallow', Then the file is allowed & the original file is returned
        """

        # Set variable for file to test
        test_file = get_file_bytes(self.doc_14kb_embedded_images)

        # Send post request
        response = requests.post(
            url=self.endpoint,
            json={
                "Base64": b64encode(test_file).decode(),
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
                "Content-Type": "application/json",
                "x-api-key": self.api_key
            }
        )

        # Status code should be 200, ok
        self.assertEqual(
            response.status_code,
            HTTPStatus.OK
        )

        # # Response content should be identical to the test file input # TODO compare to known file bytes
        # self.assertEqual(
        #     b64decode(response.content),
        #     test_file
        # )

    def test_post___bmp_32kb_content_management_policy_sanitise___returns_protected_file(self):
        """
        4-Test_The default cmp policy is applied to submitted file using base64 code
        Steps:
            Set cmp policy for file type as 'cmptype'
            Post file payload request to endpoint: '[API GATEWAY URL]/api/Rebuild/base64' with valid x-api key
        Expected:
        The response is returned with success code '200'
            0) If cmpType is 'Allow', Then the file is allowed & the original file is returned
            1) If cmpType is 'Sanitise', Then the file is returned sanitised
            2) If cmpType is 'Disallow', Then the file is allowed & the original file is returned
        """

        # Set variable for file to test
        test_file = get_file_bytes(self.doc_14kb_embedded_images)

        # Send post request
        response = requests.post(
            url=self.endpoint,
            json={
                "Base64": b64encode(test_file).decode(),
                "ContentManagementFlags": {
                    "WordContentManagement": {
                        "Metadata": 1,
                        "InternalHyperlinks": 1,
                        "ExternalHyperlinks": 1,
                        "EmbeddedFiles": 1,
                        "EmbeddedImages": 1,
                        "DynamicDataExchange": 1,
                        "Macros": 1,
                        "ReviewComments": 1
                    }
                }
            },
            headers={
                "Content-Type": "application/json",
                "x-api-key": self.api_key
            }
        )

        # Status code should be 200, ok
        self.assertEqual(
            response.status_code,
            HTTPStatus.OK
        )

        # # Response content should be identical to the test file input # TODO compare to known file bytes
        # self.assertEqual(
        #     b64decode(response.content),
        #     test_file
        # )

    @unittest.skip
    def test_post___bmp_32kb_content_management_policy_disallow___returns_status_code_200(self):
        """
        4-Test_The default cmp policy is applied to submitted file using base64 code
        Steps:
            Set cmp policy for file type as 'cmptype'
            Post file payload request to endpoint: '[API GATEWAY URL]/api/Rebuild/base64' with valid x-api key
        Expected:
        The response is returned with success code '200'
            0) If cmpType is 'Allow', Then the file is allowed & the original file is returned
            1) If cmpType is 'Sanitise', Then the file is returned sanitised
            2) If cmpType is 'Disallow', Then the file is allowed & the original file is returned
        """

        # Set variable for file to test
        test_file = get_file_bytes(self.doc_14kb_embedded_images)

        # Send post request
        response = requests.post(
            url=self.endpoint,
            json={
                "Base64": b64encode(test_file).decode(),
                "ContentManagementFlags": {
                    "WordContentManagement": {
                        "EmbeddedImages": 2,
                    }
                }
            },
            headers={
                "Content-Type": "application/json",
                "x-api-key": self.api_key
            }
        )

        # Status code should be 200, ok
        self.assertEqual(
            response.status_code,
            HTTPStatus.OK
        )

        # Response content should be empty bytes, the file contains embedded images which is set to disallow
        self.assertEqual(
            b64decode(response.content),
            b""
        )

    def test_post___txt_1kb___returns_status_code_422(self):
        """
        10-Test_unsupported file upload using base64 code & less than 6mb with valid x-api key is unsuccessful
        Execution Steps:
            Post a unsupported file payload request to endpoint: '[API GATEWAY URL]/api/Rebuild/base64' with valid x-api key
        Expected Results:
        The response message 'Unprocessable Entity' is returned with error code '422'
        """

        # Set variable for file to test
        test_file = get_file_bytes(self.txt_1kb)

        # Send post request
        response = requests.post(
            url=self.endpoint,
            json={
                "Base64": b64encode(test_file).decode()
            },
            headers={
                "Content-Type": "application/json",
                "x-api-key": self.api_key
            }
        )

        # Status code should be 422, Unprocessable Entity
        self.assertEqual(
            response.status_code,
            HTTPStatus.UNPROCESSABLE_ENTITY
        )

    def test_post___xls_48kb_malware_macro___returns_status_code_200(self):
        """
        12-Test_upload of files with issues and or malware using base64 code with valid x-api key 
        Execution Steps:
            Post a payload request with file containing malware to url: '[API GATEWAY URL]/api/Rebuild/base64' with valid x-api key
            Post a payload request with file containing structural issues to url: '[API GATEWAY URL]/api/Rebuild/base64' with valid x-api key
            Post a payload request with file containing issues and malware to url: '[API GATEWAY URL]/api/Rebuild/base64' with valid x-api key
        Expected Results:
        The response message returned for file containing malware is:'OK' with success code '200'
        The response message returned for file containing structural issues is: 'Unprocessable Entity' with error code '422'
        The response message returned for file containing malware is: 'Unprocessable Entity' with error code '422'
        """

        # Set variable for file to test
        test_file = get_file_bytes(self.xls_48kb_malware_macro)

        # Send post request
        response = requests.post(
            url=self.endpoint,
            json={
                "Base64": b64encode(test_file).decode()
            },
            headers={
                "Content-Type": "application/json",
                "x-api-key": self.api_key
            }
        )

        # Status code should be 422, Unprocessable Entity
        self.assertEqual(
            response.status_code,
            HTTPStatus.OK
        )

    def test_post___jpeg_corrupt_10kb___returns_status_code_422(self):
        """
        12-Test_upload of files with issues and or malware using base64 code with valid x-api key 
        Execution Steps:
            Post a payload request with file containing malware to url: '[API GATEWAY URL]/api/Rebuild/base64' with valid x-api key
            Post a payload request with file containing structural issues to url: '[API GATEWAY URL]/api/Rebuild/base64' with valid x-api key
            Post a payload request with file containing issues and malware to url: '[API GATEWAY URL]/api/Rebuild/base64' with valid x-api key
        Expected Results:
        The response message returned for file containing malware is:'OK' with success code '200'
        The response message returned for file containing structural issues is: 'Unprocessable Entity' with error code '422'
        The response message returned for file containing malware is: 'Unprocessable Entity' with error code '422'
        """

        # Set variable for file to test
        test_file = get_file_bytes(self.jpeg_corrupt_10kb)

        # Send post request
        response = requests.post(
            url=self.endpoint,
            json={
                "Base64": b64encode(test_file).decode()
            },
            headers={
                "Content-Type": "application/json",
                "x-api-key": self.api_key
            }
        )

        # Status code should be 422, Unprocessable Entity
        self.assertEqual(
            response.status_code,
            HTTPStatus.UNPROCESSABLE_ENTITY
        )


if __name__ == "__main__":
    unittest.main()

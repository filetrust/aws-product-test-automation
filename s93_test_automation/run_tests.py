

import logging
log = logging.getLogger("glasswall")
import os
import sys
from s93_test_automation import _ROOT
import unittest
import requests
import json


def run(product,key_type):
    test_directory = os.path.join(_ROOT, "integration_tests", product,key_type)
    log.debug("test_directory: %s", test_directory)

    test_directory_security = os.path.join(_ROOT,"security_tests")
    log.debug("test_directory: %s", test_directory_security)
    suite_security = unittest.TestLoader().discover(test_directory_security)

    #Discover tests in test_directory
    try:
        suite = unittest.TestLoader().discover(test_directory)
    except ImportError:
        raise ValueError(f"Invalid product: {product}. Expected one of: {[f.name for f in os.scandir(os.path.join(_ROOT, 'integration_tests')) if f.is_dir() and f.name != '__pycache__']}")


    # Run tests with verbosity 2
    result = unittest.TextTestRunner(verbosity=2).run(suite)

    result_security = unittest.TextTestRunner(verbosity=2).run(suite_security)

    if result.errors + result.failures + result_security.errors + result_security.failures == []:
        log.debug("Success.")
        sys.exit(0)
    else:
        if result.errors + result.failures == []:
            log.debug("Integration Tests Ok.")
        else:    
            log.warning("Failed: %s", test_directory)
            log.debug("Errors:")
            for test, msg in result.errors:
                log.debug(test)
                log.debug(msg)
            log.debug("Failures:")
            for test, msg in result.failures:
                log.debug(test)
                log.debug(msg)
        
        if result_security.errors + result_security.failures == []:
            log.debug("Security Tests Ok.")
        else:
            log.warning("Failed: %s", test_directory_security)
            log.debug("Security Errors:")
            for test, msg in result_security.errors:
                log.debug(test)
                log.debug(msg)
            log.debug("Security Failures:")
            for test, msg in result_security.failures:
                log.debug(test)
                log.debug(msg)

            response = requests.get(
                url = 'http://localhost:8080/JSON/alert/view/alertsByRisk', 
                headers = {
                    'Accept': 'application/json',
                    'X-ZAP-API-Key': os.environ["zap_api_key"]
                }
            ).json()
            print(json.dumps(response))
        sys.exit(1)

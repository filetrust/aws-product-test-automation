

import logging
log = logging.getLogger("glasswall")
import os
import sys
from s93_test_automation import _ROOT
import unittest


def run(product):
    test_directory = os.path.join(_ROOT, "integration_tests", product)
    log.debug("test_directory: %s", test_directory)

    # Discover tests in test_directory
    try:
        suite = unittest.TestLoader().discover(test_directory)
    except ImportError:
        raise ValueError(f"Invalid product: {product}. Expected one of: {[f.name for f in os.scandir(os.path.join(_ROOT, 'integration_tests')) if f.is_dir() and f.name != '__pycache__']}")

    # Run tests with verbosity 2
    result = unittest.TextTestRunner(verbosity=2).run(suite)

    if result.errors + result.failures == []:
        log.debug("Success.")
        sys.exit(0)
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
        sys.exit(1)

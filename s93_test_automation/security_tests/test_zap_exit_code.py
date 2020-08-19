import sys
import requests
import json
import unittest
import logging

class Test_rebuild_security(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.zap_api_key = os.environ["zap_api_key"]

  @classmethod
  def tearDownClass(cls):
    pass

  def setUp(self):
    pass
  
  def tearDown(self):
    pass

  def test_get_security_high_risk_returns_0_(self):

    response = requests.get(
      url = 'http://localhost:8080/JSON/alert/view/alertCountsByRisk', 
      headers = {
        'Accept': 'application/json',
        'X-ZAP-API-Key': self.zap_api_key
      }
    ).json()

    ## Retrive
    High=response['High']

    self.assertEqual(
      High,
      0
    )

  def test_get_security_medium_risk_returns_0_(self):

    response = requests.get(
      url = 'http://localhost:8080/JSON/alert/view/alertCountsByRisk', 
      headers = {
        'Accept': 'application/json',
        'X-ZAP-API-Key': self.zap_api_key
      }
    ).json()

    Medium=response['Medium']

    self.assertEqual(
      Medium,
      0
    )

  def test_get_security_low_risk_returns_0_(self):

    response = requests.get(
      url = 'http://localhost:8080/JSON/alert/view/alertCountsByRisk', 
      headers = {
        'Accept': 'application/json',
        'X-ZAP-API-Key': self.zap_api_key
      }
    ).json()

    Low=response['Low']

    self.assertEqual(
      Low,
      0
    )


if __name__ == "__main__":
    unittest.main()

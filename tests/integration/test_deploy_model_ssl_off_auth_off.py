import integ_test_base
import subprocess
from pathlib import Path


class TestDeployModelSSLOffAuthOff(integ_test_base.IntegTestBase):
    def test_deploy_ssl_off_auth_off(self):
        self.deploy_models(self._get_username(), self._get_password())

        conn = self._get_connection()

        models = ['PCA', 'Sentiment%20Analysis', "ttest"]
        for m in models:
            conn.request("GET", f'/endpoints/{m}')
            m_request = conn.getresponse()
            self.assertEqual(200, m_request.status)
            m_request.read()

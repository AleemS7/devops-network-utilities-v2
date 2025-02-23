import pytest
import sys
import os
from unittest.mock import patch

root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.join(root_dir, "src", "network_diagnostics", "cli"))

import diag

@pytest.mark.parametrize("target,count", [
    ("google.com", 1),
    ("8.8.8.8", 2)
])
@patch("subprocess.run")
def test_ping(mock_run, target, count):
    mock_run.return_value.stdout = "Mock ping output"
    mock_run.return_value.stderr = ""
    mock_run.return_value.returncode = 0

    result = diag.ping(target, count)
    # We only check that subprocess was called correctly; 
    # actual output is system-dependent.
    mock_run.assert_called_once()

@patch("subprocess.run")
def test_traceroute(mock_run):
    mock_run.return_value.stdout = "Mock traceroute output"
    mock_run.return_value.stderr = ""
    mock_run.return_value.returncode = 0

    result = diag.traceroute("google.com")
    mock_run.assert_called_once()

@patch("subprocess.run")
def test_dns_lookup(mock_run):
    mock_run.return_value.stdout = "Mock nslookup output"
    mock_run.return_value.stderr = ""
    mock_run.return_value.returncode = 0

    result = diag.dns_lookup("google.com")
    mock_run.assert_called_once()

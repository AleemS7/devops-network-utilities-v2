import React, { useState } from 'react';
import './App.css';

/**
 * Environment variables (for Docker Compose):
 *   REACT_APP_SUBNET_URL=http://subnet-web:5000
 *   REACT_APP_DIAG_URL=http://diag-web:5001
 * Fallback to localhost if not set.
 */
const subnetBase = process.env.REACT_APP_SUBNET_URL || 'http://localhost:5000';
const diagBase   = process.env.REACT_APP_DIAG_URL   || 'http://localhost:5001';

function App() {
  /************************************************************************
   * Subnet Calculator States
   ************************************************************************/
  const [subnetIp, setSubnetIp] = useState('');
  const [subnetCidr, setSubnetCidr] = useState('24');
  const [subnetResult, setSubnetResult] = useState<any>(null);
  const [subnetError, setSubnetError] = useState('');
  const [subnetLoading, setSubnetLoading] = useState(false);

  /************************************************************************
   * Network Diagnostics States
   ************************************************************************/
  const [diagMethod, setDiagMethod] = useState('ping'); // "ping" | "traceroute" | "dns" | "scan"
  const [diagTarget, setDiagTarget] = useState('');
  const [diagResult, setDiagResult] = useState<any>(null);
  const [diagError, setDiagError] = useState('');
  const [diagLoading, setDiagLoading] = useState(false);

  // Port scan specific
  const [scanStart, setScanStart] = useState('1');
  const [scanEnd, setScanEnd] = useState('1024');

  /************************************************************************
   * Handlers: Subnet Calculator
   ************************************************************************/
  const handleSubnetCalculate = async () => {
    setSubnetError('');
    setSubnetResult(null);
    setSubnetLoading(true);

    try {
      const response = await fetch(
        `${subnetBase}/calculate?ip=${subnetIp}&subnet=${subnetCidr}`
      );
      if (!response.ok) {
        const errorData = await response.json();
        setSubnetError(errorData.error || 'Error calculating subnet.');
      } else {
        const data = await response.json();
        setSubnetResult(data);
      }
    } catch (error: any) {
      setSubnetError(error.message || 'Network error.');
    } finally {
      setSubnetLoading(false);
    }
  };

  /************************************************************************
   * Handlers: Network Diagnostics
   ************************************************************************/
  const handleDiagnostics = async () => {
    setDiagError('');
    setDiagResult(null);
    setDiagLoading(true);

    try {
      let url = '';
      switch (diagMethod) {
        case 'ping':
          url = `${diagBase}/ping?target=${diagTarget}&count=2`;
          break;
        case 'traceroute':
          url = `${diagBase}/traceroute?target=${diagTarget}`;
          break;
        case 'dns':
          url = `${diagBase}/dns?domain=${diagTarget}`;
          break;
        case 'scan':
          url = `${diagBase}/scan?host=${diagTarget}&start=${scanStart}&end=${scanEnd}`;
          break;
        default:
          url = `${diagBase}/ping?target=${diagTarget}&count=2`; // fallback
      }

      const response = await fetch(url);
      if (!response.ok) {
        const errorData = await response.json();
        setDiagError(errorData.error || 'Error performing diagnostics.');
      } else {
        const data = await response.json();
        setDiagResult(data);
      }
    } catch (error: any) {
      setDiagError(error.message || 'Network error.');
    } finally {
      setDiagLoading(false);
    }
  };

  /************************************************************************
   * Render Helpers
   ************************************************************************/
  const renderSubnetResult = () => {
    if (subnetLoading) {
      return <p className="loading">Calculating subnet...</p>;
    }
    if (subnetError) {
      return <p className="error-message">{subnetError}</p>;
    }
    if (subnetResult) {
      return (
        <div className="result-box">
          <h3>Subnet Calculation Result</h3>
          <p><strong>Network:</strong> {subnetResult.network}</p>
          <p><strong>Network Address:</strong> {subnetResult.network_address}</p>
          <p><strong>Broadcast Address:</strong> {subnetResult.broadcast_address}</p>
          <p><strong>Number of Hosts:</strong> {subnetResult.number_of_hosts}</p>
        </div>
      );
    }
    return null;
  };

  const renderDiagnosticsResult = () => {
    if (diagLoading) {
      return <p className="loading">Running {diagMethod}...</p>;
    }
    if (diagError) {
      return <p className="error-message">{diagError}</p>;
    }
    if (!diagResult) {
      return null;
    }

    // Different display logic based on diagMethod
    switch (diagMethod) {
      case 'ping':
      case 'traceroute':
      case 'dns':
        if (diagResult.output) {
          // Split lines for easier reading
          const lines = diagResult.output.split('\n');
          return (
            <div className="result-box">
              <h3>{diagMethod.toUpperCase()} Output</h3>
              {lines.map((line: string, idx: number) => (
                <div key={idx}>{line}</div>
              ))}
            </div>
          );
        }
        break;

      case 'scan':
        if (diagResult.open_ports) {
          return (
            <div className="result-box">
              <h3>Open Ports</h3>
              {diagResult.open_ports.length > 0 ? (
                <ul>
                  {diagResult.open_ports.map((port: number) => (
                    <li key={port}>{port}</li>
                  ))}
                </ul>
              ) : (
                <p>No open ports found.</p>
              )}
            </div>
          );
        }
        break;
      default:
        // fallback
        return (
          <div className="result-box">
            <pre>{JSON.stringify(diagResult, null, 2)}</pre>
          </div>
        );
    }

    // If we didn't handle it above, just show raw JSON
    return (
      <div className="result-box">
        <pre>{JSON.stringify(diagResult, null, 2)}</pre>
      </div>
    );
  };

  return (
    <div className="app-container">
      <header>
        <h1>Network Utilities</h1>
      </header>

      <main>
        {/* SUBNET CALCULATOR */}
        <section className="section-card">
          <h2>Subnet Calculator</h2>
          <div className="form-row">
            <label htmlFor="subnetIp">IP Address:</label>
            <input
              id="subnetIp"
              type="text"
              placeholder="e.g. 192.168.1.0"
              value={subnetIp}
              onChange={(e) => setSubnetIp(e.target.value)}
            />
          </div>
          <div className="form-row">
            <label htmlFor="subnetCidr">CIDR:</label>
            <input
              id="subnetCidr"
              type="number"
              placeholder="24"
              value={subnetCidr}
              onChange={(e) => setSubnetCidr(e.target.value)}
            />
          </div>
          <button onClick={handleSubnetCalculate}>Calculate</button>
          {renderSubnetResult()}
        </section>

        {/* NETWORK DIAGNOSTICS */}
        <section className="section-card">
          <h2>Network Diagnostics</h2>
          <div className="form-row">
            <label htmlFor="diagMethod">Method:</label>
            <select
              id="diagMethod"
              value={diagMethod}
              onChange={(e) => setDiagMethod(e.target.value)}
            >
              <option value="ping">Ping</option>
              <option value="traceroute">Traceroute</option>
              <option value="dns">DNS Lookup</option>
              <option value="scan">Port Scan</option>
            </select>
          </div>
          <div className="form-row">
            <label htmlFor="diagTarget">
              {diagMethod === 'scan' ? 'Host (IP/Domain):' : 'Target/Domain/IP:'}
            </label>
            <input
              id="diagTarget"
              type="text"
              placeholder="e.g. google.com or 8.8.8.8"
              value={diagTarget}
              onChange={(e) => setDiagTarget(e.target.value)}
            />
          </div>

          {/* Additional fields if port scan is selected */}
          {diagMethod === 'scan' && (
            <>
              <div className="form-row">
                <label htmlFor="scanStart">Start Port:</label>
                <input
                  id="scanStart"
                  type="number"
                  value={scanStart}
                  onChange={(e) => setScanStart(e.target.value)}
                />
              </div>
              <div className="form-row">
                <label htmlFor="scanEnd">End Port:</label>
                <input
                  id="scanEnd"
                  type="number"
                  value={scanEnd}
                  onChange={(e) => setScanEnd(e.target.value)}
                />
              </div>
            </>
          )}

          <button onClick={handleDiagnostics}>Run</button>
          {renderDiagnosticsResult()}
        </section>
      </main>

      <footer>
        <p>Built by Aleem.</p>
      </footer>
    </div>
  );
}

export default App;

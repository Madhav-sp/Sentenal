import React, { useState } from "react";
import axios from "axios";

function App() {
  const [domain, setDomain] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [stage, setStage] = useState("");

  const fakeProgress = async () => {
    const steps = [
      "Discovering subdomains...",
      "Resolving infrastructure...",
      "Analyzing risks...",
      "Generating AI intelligence..."
    ];

    for (let step of steps) {
      setStage(step);
      await new Promise((r) => setTimeout(r, 1200));
    }
  };

  const scan = async () => {
    try {
      setLoading(true);
      setResult(null);

      // start fake progress animation
      fakeProgress();

      const res = await axios.post("http://localhost:8000/scan", {
        domain,
      });

      const id = res.data.scan_id;

      const resultRes = await axios.get(
        `http://localhost:8000/result/${id}`
      );

      setResult(resultRes.data);
    } catch (err) {
      console.error(err);
      alert("Scan failed");
    } finally {
      setLoading(false);
      setStage("");
    }
  };

  return (
    <div style={styles.container}>
      <h1>AI Attack Surface Intelligence</h1>

      <input
        value={domain}
        onChange={(e) => setDomain(e.target.value)}
        placeholder="example.com"
        style={styles.input}
      />

      <button onClick={scan} style={styles.button}>
        Analyze
      </button>

      {loading && (
        <div style={styles.loader}>
          <div className="spinner" />
          <p>{stage}</p>
        </div>
      )}

      {result && (
        <div style={styles.result}>
          <h2>Risk Score: {result.risk_score}</h2>

          <h3>AI Summary</h3>
          <p>{result.ai_summary}</p>

          <h3>Assets</h3>
          {result.assets.map((a, i) => (
            <div key={i}>
              {a.subdomain} — <b>{a.severity}</b>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

const styles = {
  container: {
    minHeight: "100vh",
    background: "#020617",
    color: "white",
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    paddingTop: "80px",
    fontFamily: "Arial",
  },
  input: {
    padding: "10px",
    margin: "10px",
    width: "250px",
  },
  button: {
    padding: "10px 20px",
    cursor: "pointer",
  },
  loader: {
    marginTop: "30px",
    textAlign: "center",
  },
  result: {
    marginTop: "40px",
    width: "60%",
  },
};

export default App;
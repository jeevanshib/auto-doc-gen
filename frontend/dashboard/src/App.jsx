import React, { useState } from "react"
import { generateDocs } from "./api"

import FilesChanged from "./components/FilesChanged"
import APIPanel from "./components/APIPanel"
import SummaryPanel from "./components/SummaryPanel"

function App() {
  const [data, setData] = useState(null)
  const [error, setError] = useState("")
  const [loading, setLoading] = useState(false)

  async function run() {
    setLoading(true)
    setError("")

    try {
      const result = await generateDocs()
      setData(result)
    } catch (requestError) {
      setData(null)
      setError(requestError.message)
    } finally {
      setLoading(false)
    }
  }

  const filesCount = data?.files?.length || 0
  const apiCount = data?.apis?.length || 0
  const commitLabel = data?.commit || "Waiting for analysis"

  return (
    <div className="app-shell">
      <div className="app-backdrop app-backdrop-left" />
      <div className="app-backdrop app-backdrop-right" />

      <main className="dashboard">
        <section className="hero-card">
          <div className="hero-copy">
            <p className="eyebrow">LOCAL AI DOCS ENGINEER</p>
            <h1>Turn raw commits into something your team can actually read.</h1>
            <p className="hero-text">
              Analyze the latest git diff, extract touched files and API routes,
              and generate a compact engineering summary through Ollama.
            </p>

            <div className="hero-actions">
              <button className="primary-button" onClick={run} disabled={loading}>
                {loading ? "Analyzing latest commit..." : "Analyze Latest Commit"}
              </button>
              <div className="commit-pill">
                <span className="commit-pill-label">Commit</span>
                <strong>{commitLabel}</strong>
              </div>
            </div>
          </div>

          <div className="hero-metrics">
            <div className="metric-card">
              <span className="metric-label">Files detected</span>
              <strong className="metric-value">{filesCount}</strong>
            </div>
            <div className="metric-card">
              <span className="metric-label">API routes</span>
              <strong className="metric-value">{apiCount}</strong>
            </div>
            <div className="metric-card metric-card-accent">
              <span className="metric-label">Generator state</span>
              <strong className="metric-value">
                {loading ? "Running" : data ? "Ready" : "Idle"}
              </strong>
            </div>
          </div>
        </section>

        {error ? <div className="status-banner status-error">{error}</div> : null}
        {data?.message ? <div className="status-banner status-info">{data.message}</div> : null}

        <section className="content-grid">
          <SummaryPanel summary={data?.summary || ""} />
          <FilesChanged files={data?.files || []} />
          <APIPanel apis={data?.apis || []} />
        </section>
      </main>
    </div>
  )
}

export default App

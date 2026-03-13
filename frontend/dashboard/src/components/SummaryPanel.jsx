import React from "react"

function SummaryPanel({ summary }) {
  return (
    <section className="panel panel-summary">
      <div className="panel-header">
        <p className="panel-kicker">AI Summary</p>
        <h2>Generated Documentation</h2>
      </div>

      {summary ? (
        <pre className="summary-output">{summary}</pre>
      ) : (
        <p className="panel-empty">
          Run the generator to turn the latest commit diff into a compact technical
          summary.
        </p>
      )}
    </section>
  )
}

export default SummaryPanel

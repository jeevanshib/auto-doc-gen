import React from "react"

function APIPanel({ apis }) {
  return (
    <section className="panel">
      <div className="panel-header">
        <p className="panel-kicker">Route Detection</p>
        <h2>Detected APIs</h2>
      </div>

      {apis.length ? (
        <ul className="token-list">
          {apis.map((api, index) => (
            <li key={`${api}-${index}`} className="token-item token-item-accent">
              {api}
            </li>
          ))}
        </ul>
      ) : (
        <p className="panel-empty">No API routes were detected in the latest code changes.</p>
      )}
    </section>
  )
}

export default APIPanel

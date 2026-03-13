import React from "react"

function FilesChanged({ files }) {
  return (
    <section className="panel">
      <div className="panel-header">
        <p className="panel-kicker">Change Scope</p>
        <h2>Files Changed</h2>
      </div>

      {files.length ? (
        <ul className="token-list">
          {files.map((file, index) => (
            <li key={`${file}-${index}`} className="token-item">
              {file}
            </li>
          ))}
        </ul>
      ) : (
        <p className="panel-empty">No code files were detected in the latest diff.</p>
      )}
    </section>
  )
}

export default FilesChanged

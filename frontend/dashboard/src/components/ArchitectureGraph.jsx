import React, { useEffect, useState } from "react"

import { getArchitecture } from "../api"

const GROUP_ORDER = ["backend", "frontend/core", "frontend/components", "scripts"]

function sortGroups(groups) {
  return [...groups].sort((left, right) => {
    const leftIndex = GROUP_ORDER.indexOf(left)
    const rightIndex = GROUP_ORDER.indexOf(right)

    if (leftIndex === -1 && rightIndex === -1) {
      return left.localeCompare(right)
    }

    if (leftIndex === -1) {
      return 1
    }

    if (rightIndex === -1) {
      return -1
    }

    return leftIndex - rightIndex
  })
}

function ArchitectureGraph() {
  const [graph, setGraph] = useState({ nodes: [], edges: [], groups: [] })
  const [error, setError] = useState("")

  useEffect(() => {
    async function load() {
      try {
        const data = await getArchitecture()
        setGraph(data)
      } catch (requestError) {
        setError(requestError.message)
      }
    }

    load()
  }, [])

  const nodes = graph.nodes || []
  const edges = graph.edges || []
  const groups = sortGroups(graph.groups || [])

  if (error) {
    return (
      <section className="panel panel-architecture">
        <div className="panel-header">
          <p className="panel-kicker">Repository Graph</p>
          <h2>Architecture Map</h2>
        </div>
        <p className="panel-empty">{error}</p>
      </section>
    )
  }

  if (!nodes.length) {
    return (
      <section className="panel panel-architecture">
        <div className="panel-header">
          <p className="panel-kicker">Repository Graph</p>
          <h2>Architecture Map</h2>
        </div>
        <p className="panel-empty">No local modules were mapped for this repository yet.</p>
      </section>
    )
  }

  const width = Math.max(980, groups.length * 270)
  const cardWidth = 196
  const cardHeight = 54
  const topPadding = 92
  const leftPadding = 88
  const rowGap = 88
  const columnGap = groups.length > 1 ? (width - leftPadding * 2) / (groups.length - 1) : 0
  const positions = {}
  let maxBottom = 320

  groups.forEach((group, groupIndex) => {
    const groupNodes = nodes
      .filter((node) => node.group === group)
      .sort((left, right) => left.path.localeCompare(right.path))

    groupNodes.forEach((node, nodeIndex) => {
      const x = leftPadding + groupIndex * columnGap
      const y = topPadding + nodeIndex * rowGap
      positions[node.id] = { x, y }
      maxBottom = Math.max(maxBottom, y + cardHeight + 42)
    })
  })

  const visibleEdges = edges.filter((edge) => positions[edge.from] && positions[edge.to])

  return (
    <section className="panel panel-architecture">
      <div className="panel-header architecture-header">
        <div>
          <p className="panel-kicker">Repository Graph</p>
          <h2>Architecture Map</h2>
        </div>
        <div className="architecture-stats">
          <span>{nodes.length} modules</span>
          <span>{visibleEdges.length} resolved links</span>
        </div>
      </div>

      <div className="architecture-legend">
        {groups.map((group) => (
          <span key={group} className="architecture-legend-item">
            {group}
          </span>
        ))}
      </div>

      <div className="architecture-canvas-wrap">
        <svg
          viewBox={`0 0 ${width} ${maxBottom}`}
          className="architecture-canvas"
          role="img"
          aria-label="Repository architecture map"
        >
          <defs>
            <linearGradient id="architectureEdge" x1="0%" y1="0%" x2="100%" y2="0%">
              <stop offset="0%" stopColor="rgba(255, 138, 92, 0.4)" />
              <stop offset="100%" stopColor="rgba(86, 182, 255, 0.45)" />
            </linearGradient>
          </defs>

          {groups.map((group) => {
            const groupNode = nodes.find((node) => node.group === group)
            if (!groupNode) {
              return null
            }

            const { x } = positions[groupNode.id]
            return (
              <g key={group}>
                <text x={x} y="38" textAnchor="middle" className="architecture-group-title">
                  {group}
                </text>
                <line
                  x1={x}
                  y1="52"
                  x2={x}
                  y2={maxBottom - 24}
                  className="architecture-group-line"
                />
              </g>
            )
          })}

          {visibleEdges.map((edge, index) => {
            const source = positions[edge.from]
            const target = positions[edge.to]
            const startX = source.x + cardWidth / 2
            const startY = source.y
            const endX = target.x - cardWidth / 2
            const endY = target.y
            const delta = Math.abs(endX - startX) * 0.45 + 40

            return (
              <path
                key={`${edge.from}-${edge.to}-${index}`}
                d={`M ${startX} ${startY} C ${startX + delta} ${startY}, ${endX - delta} ${endY}, ${endX} ${endY}`}
                className="architecture-edge-path"
              />
            )
          })}

          {nodes.map((node) => {
            const position = positions[node.id]
            if (!position) {
              return null
            }

            const shortPath = node.path.replace("frontend/dashboard/src/", "src/")

            return (
              <g
                key={node.id}
                transform={`translate(${position.x - cardWidth / 2}, ${position.y - cardHeight / 2})`}
              >
                <rect width={cardWidth} height={cardHeight} rx="16" className="architecture-node-card" />
                <text x="18" y="23" className="architecture-node-label">
                  {node.label}
                </text>
                <text x="18" y="40" className="architecture-node-path">
                  {shortPath}
                </text>
              </g>
            )
          })}
        </svg>
      </div>
    </section>
  )
}

export default ArchitectureGraph

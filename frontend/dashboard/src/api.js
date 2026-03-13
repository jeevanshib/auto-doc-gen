export async function generateDocs() {
  const response = await fetch("http://localhost:8000/generate", {
    method: "POST",
  })

  const payload = await response.json()

  if (!response.ok) {
    throw new Error(payload.detail || "Failed to generate documentation")
  }

  return payload
}

export async function getHistory() {
  const response = await fetch("http://localhost:8000/history")
  const payload = await response.json()

  if (!response.ok) {
    throw new Error(payload.detail || "Failed to load history")
  }

  return payload
}

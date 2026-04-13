const BASE_URL = 'http://localhost:4000'

const headers = { 'Content-Type': 'application/json' }

export const api = {
  async get(path) {
    const res = await fetch(`${BASE_URL}${path}`)
    return res.json()
  },
  async post(path, data) {
    const res = await fetch(`${BASE_URL}${path}`, {
      method: 'POST',
      headers,
      body: JSON.stringify(data || {})
    })
    return res.json()
  },
  async put(path, data) {
    const res = await fetch(`${BASE_URL}${path}`, {
      method: 'PUT',
      headers,
      body: JSON.stringify(data || {})
    })
    return res.json()
  },
  async del(path) {
    const res = await fetch(`${BASE_URL}${path}`, {
      method: 'DELETE'
    })
    return res.json()
  }
}

import { useEffect, useState } from 'react'

function App() {
  const [pages, setPages] = useState([])
  const [result, setResult] = useState('')
  const [inputText, setInputText] = useState('')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(false)

  useEffect(() => {
    fetch('/api/pages')
      .then(res => res.json())
      .then(data => {
        setPages(data) // direct array response
        setLoading(false)
      })
      .catch(() => {
        setPages([])
        setError(true)
        setLoading(false)
      })
  }, [])
  

  const doPlaywright = async (page) => {
    try {
      const response = await fetch('/doPlaywright', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ page }),
      })
      const data = await response.json()
      setResult(JSON.stringify(data, null, 2))
    } catch (err) {
      setResult('Error calling Playwright | ' + err)
    }
  }

  const sendToServer = async () => {
    try {
      const response = await fetch('/echo', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: inputText }),
      })
      const data = await response.json()
      setResult(JSON.stringify(data, null, 2))
    } catch (err) {
      setResult('Error calling Echo | ' + err)
    }
  }

  return (
    <div style={{ padding: '2rem', fontFamily: 'sans-serif' }}>
      <h1>Available Pages</h1>

      {loading && <p>Loading pages...</p>}
      {error && <p style={{ color: 'red' }}>Failed to load pages.</p>}

      {!loading && !error && pages.length === 0 && <p>No pages found.</p>}

      <div style={{ display: 'flex', flexWrap: 'wrap', gap: '1rem' }}>
        {pages.map(page => (
          <button
            key={page}
            onClick={() => doPlaywright(page)}
            style={{ padding: '0.5rem 1rem', fontSize: '1rem' }}
          >
            {page}
          </button>
        ))}
      </div>

      <hr style={{ margin: '2rem 0' }} />

      <h2>Test Echo API</h2>
      <input
        type="text"
        value={inputText}
        onChange={e => setInputText(e.target.value)}
        placeholder="Type something..."
        style={{ padding: '0.5rem', fontSize: '1rem', marginRight: '0.5rem' }}
      />
      <button onClick={sendToServer} style={{ padding: '0.5rem 1rem' }}>
        Send
      </button>

      <pre style={{ marginTop: '2rem', background: '#f4f4f4', padding: '1rem' }}>
        {result}
      </pre>
    </div>
  )
}

export default App

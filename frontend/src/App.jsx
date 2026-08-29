import { useEffect, useState } from 'react'
import { getHealth } from './api/health'

function App() {
  const [health, setHealth] = useState(null)
  const [error, setError] = useState(null)

  useEffect(() => {
    getHealth()
      .then(setHealth)
      .catch((err) => setError(err.message))
  }, [])

  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-50">
      <div className="text-center">
        <h1 className="text-3xl font-bold text-slate-800 mb-4">
          Frontend foundation ready
        </h1>
        {error && (
          <p className="text-red-600">Backend connection failed: {error}</p>
        )}
        {health && (
          <p className="text-green-700">
            Backend says: {health.status} ({health.service})
          </p>
        )}
      </div>
    </div>
  )
}

export default App
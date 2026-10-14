import {useContext, useState} from 'react'
import {Link, Navigate, useNavigate} from 'react-router'
import {apiFetch, getErrorMessage} from '../api'
import {AppContext} from '../context'

const Login = () => {
  const {loggedIn, login} = useContext(AppContext)
  const navigate = useNavigate()
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [busy, setBusy] = useState(false)

  if (loggedIn) return <Navigate to="/listings" replace />

  const onSubmit = async e => {
    e.preventDefault()
    setBusy(true)
    setError('')
    try {
      const res = await apiFetch('/api/users/login/', {method: 'POST', body: JSON.stringify({username, password})})
      const data = await res.json()
      if (res.ok) {
        login(data)
        navigate('/listings')
      } else {
        setError(getErrorMessage(data)) // login errors use "detail"
      }
    } catch {
      setError('Cannot reach the server. Is Django running on port 8000?')
    }
    setBusy(false)
  }

  return (
    <form className="panel narrow" onSubmit={onSubmit}>
      <h1>Log in</h1>
      <label>Username<input value={username} onChange={e => setUsername(e.target.value)} required /></label>
      <label>Password<input type="password" value={password} onChange={e => setPassword(e.target.value)} required /></label>
      {error && <p className="error-text" role="alert">{error}</p>}
      <button className="btn" disabled={busy}>{busy ? 'Logging in…' : 'Log in'}</button>
      <p className="muted">New here? <Link to="/register">Create an account</Link></p>
      <p className="hint">Demo: Priya / secret123 (seller), Arjun / secret123 (student)</p>
    </form>
  )
}

export default Login

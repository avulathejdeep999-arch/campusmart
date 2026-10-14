import {useState} from 'react'
import {Link, useNavigate} from 'react-router'
import {apiFetch, getErrorMessage} from '../api'

const Register = () => {
  const navigate = useNavigate()
  const [form, setForm] = useState({username: '', email: '', password: '', confirmPassword: '', user_type: 'student'})
  const [error, setError] = useState('')
  const [busy, setBusy] = useState(false)
  const set = k => e => setForm({...form, [k]: e.target.value})

  const onSubmit = async e => {
    e.preventDefault()
    if (form.password !== form.confirmPassword) {
      setError('The two passwords do not match.') // the one rule that never reaches the server
      return
    }
    setBusy(true)
    setError('')
    const {username, email, password, user_type} = form // confirmPassword is NOT sent
    try {
      const res = await apiFetch('/api/users/register/', {method: 'POST', body: JSON.stringify({username, email, password, user_type})})
      const data = await res.json()
      if (res.ok) navigate('/login') // registering is not logging in
      else setError(getErrorMessage(data)) // register errors use the field name
    } catch {
      setError('Cannot reach the server. Is Django running on port 8000?')
    }
    setBusy(false)
  }

  return (
    <form className="panel narrow" onSubmit={onSubmit}>
      <h1>Create account</h1>
      <label>Username<input value={form.username} onChange={set('username')} required /></label>
      <label>Email<input type="email" value={form.email} onChange={set('email')} /></label>
      <label>Password<input type="password" minLength={6} value={form.password} onChange={set('password')} required /></label>
      <label>Confirm password<input type="password" value={form.confirmPassword} onChange={set('confirmPassword')} required /></label>
      <label>I want to
        <select value={form.user_type} onChange={set('user_type')}>
          <option value="student">Buy things</option>
          <option value="seller">Buy and sell things</option>
        </select>
      </label>
      {error && <p className="error-text" role="alert">{error}</p>}
      <button className="btn" disabled={busy}>{busy ? 'Creating…' : 'Create account'}</button>
      <p className="muted">Already registered? <Link to="/login">Log in</Link></p>
    </form>
  )
}

export default Register

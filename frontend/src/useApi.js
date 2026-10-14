import {useEffect, useState} from 'react'
import {apiFetch, getErrorMessage} from './api'

// GET helper. Returns {data, status, error, loading}. `path` null means "do not fetch".
const useApi = (path, deps = []) => {
  const [state, setState] = useState({data: null, status: 0, error: '', loading: true})
  useEffect(() => {
    if (path === null) return undefined
    let alive = true
    setState(s => ({...s, loading: true, error: ''}))
    apiFetch(path)
      .then(async res => {
        const data = res.status === 204 ? null : await res.json().catch(() => null)
        if (!alive) return
        setState({data: res.ok ? data : null, status: res.status, error: res.ok ? '' : getErrorMessage(data), loading: false})
      })
      .catch(() => alive && setState({data: null, status: 0, error: 'Cannot reach the server. Is Django running on port 8000?', loading: false}))
    return () => {
      alive = false
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [path, ...deps])
  return state
}

export default useApi

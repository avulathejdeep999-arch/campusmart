import {useContext} from 'react'
import {Navigate, Outlet} from 'react-router'
import {AppContext} from '../context'

// Politeness only - the real lock is in Django.
const ProtectedRoute = () => {
  const {loggedIn} = useContext(AppContext)
  return loggedIn ? <Outlet /> : <Navigate to="/login" replace />
}

export default ProtectedRoute

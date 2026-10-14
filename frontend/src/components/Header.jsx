import {useContext} from 'react'
import {Link, NavLink, useNavigate} from 'react-router'
import {FiShoppingCart} from 'react-icons/fi'
import {AppContext} from '../context'

const Header = () => {
  const {loggedIn, logout, cartItems} = useContext(AppContext)
  const navigate = useNavigate()
  const count = cartItems.reduce((n, i) => n + i.quantity, 0)
  const onLogout = async () => {
    await logout()
    navigate('/login')
  }
  return (
    <header className="header">
      <Link to="/" className="brand">Campus<span>Mart</span></Link>
      <nav>
        <NavLink to="/listings">Browse</NavLink>
        {loggedIn && <NavLink to="/orders">My orders</NavLink>}
        {loggedIn && <NavLink to="/seller">Sell</NavLink>}
        {loggedIn && (
          <NavLink to="/cart" className="cart-link" aria-label="Cart">
            <FiShoppingCart /> {count > 0 && <b className="badge">{count}</b>}
          </NavLink>
        )}
        {loggedIn ? (
          <button type="button" className="btn ghost" onClick={onLogout}>Log out</button>
        ) : (
          <>
            <NavLink to="/login">Log in</NavLink>
            <Link to="/register" className="btn">Create account</Link>
          </>
        )}
      </nav>
    </header>
  )
}

export default Header

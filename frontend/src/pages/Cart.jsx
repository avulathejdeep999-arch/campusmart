import {useContext} from 'react'
import {Link, useNavigate} from 'react-router'
import {money} from '../api'
import {AppContext} from '../context'

const Cart = () => {
  const {cartItems, updateCartItem, removeCartItem} = useContext(AppContext)
  const navigate = useNavigate()
  const total = cartItems.reduce((sum, i) => sum + i.price * i.quantity, 0)

  if (cartItems.length === 0) {
    return <div className="empty"><h2>Your cart is empty</h2><Link className="btn" to="/listings">Find something to buy</Link></div>
  }
  return (
    <>
      <h1>Your cart</h1>
      <ul className="rows">
        {cartItems.map(i => (
          <li key={i.id} className="row-item">
            <img src={i.image} alt="" />
            <div className="grow"><Link to={`/listings/${i.listingId}`}><b>{i.title}</b></Link><p className="muted">{i.condition} · {money(i.price)} each</p></div>
            <div className="stepper">
              <button type="button" aria-label="Decrease" onClick={() => updateCartItem(i.id, i.quantity - 1)}>−</button>
              <span>{i.quantity}</span>
              <button type="button" aria-label="Increase" onClick={() => updateCartItem(i.id, i.quantity + 1)}>+</button>
            </div>
            <strong>{money(i.price * i.quantity)}</strong>
            <button type="button" className="btn ghost" onClick={() => removeCartItem(i.id)}>Remove</button>
          </li>
        ))}
      </ul>
      <div className="total-bar"><span>Total</span><strong>{money(total)}</strong><button type="button" className="btn" onClick={() => navigate('/checkout')}>Checkout</button></div>
    </>
  )
}

export default Cart

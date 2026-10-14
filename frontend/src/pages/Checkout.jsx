import {useContext, useState} from 'react'
import {Link, useNavigate} from 'react-router'
import {apiFetch, getErrorMessage, money} from '../api'
import {AppContext} from '../context'

const FIELDS = [['full_name', 'Full name'], ['phone', 'Phone (10 digits)'], ['address', 'Address'], ['city', 'City'], ['state', 'State'], ['pincode', 'Pincode (6 digits)']]
const MEETUPS = [['MAIN_GATE', 'Main Gate'], ['LIBRARY', 'Library Steps'], ['CANTEEN', 'Canteen']]

const Checkout = () => {
  const {cartItems, getCart} = useContext(AppContext)
  const navigate = useNavigate()
  const [address, setAddress] = useState(Object.fromEntries(FIELDS.map(([k]) => [k, ''])))
  const [payment, setPayment] = useState('COD')
  const [meetup, setMeetup] = useState('MAIN_GATE')
  const [error, setError] = useState('')
  const [busy, setBusy] = useState(false)
  const total = cartItems.reduce((s, i) => s + i.price * i.quantity, 0)

  if (cartItems.length === 0) return <div className="empty"><h2>Nothing to check out</h2><Link className="btn" to="/listings">Browse listings</Link></div>

  const onSubmit = async e => {
    e.preventDefault()
    setBusy(true)
    setError('')
    // Only three things are sent: payment method, meetup point, address. Never the cart or the total.
    const res = await apiFetch('/api/orders/', {method: 'POST', body: JSON.stringify({payment_method: payment, meetup_point: meetup, address})})
    const data = await res.json().catch(() => null)
    if (res.status === 201) {
      await getCart()
      navigate(`/orders/${data.id}`)
    } else {
      setError(getErrorMessage(data))
      setBusy(false)
    }
  }

  return (
    <form className="checkout" onSubmit={onSubmit}>
      <section className="panel">
        <h1>Checkout</h1>
        {FIELDS.map(([k, label]) => (
          <label key={k}>{label}<input value={address[k]} onChange={e => setAddress({...address, [k]: e.target.value})} required /></label>
        ))}
        <fieldset><legend>Payment</legend>
          <label className="opt"><input type="radio" checked={payment === 'COD'} onChange={() => setPayment('COD')} /> Cash at Meetup</label>
          <label className="opt"><input type="radio" checked={payment === 'ONLINE'} onChange={() => setPayment('ONLINE')} /> Pay Now</label>
        </fieldset>
        <label>Meetup point
          <select value={meetup} onChange={e => setMeetup(e.target.value)}>{MEETUPS.map(([v, l]) => <option key={v} value={v}>{l}</option>)}</select>
        </label>
      </section>
      <section className="panel">
        <h2>Your items</h2>
        <ul className="plain">{cartItems.map(i => <li key={i.id} className="row"><span>{i.title} × {i.quantity}</span><span>{money(i.price * i.quantity)}</span></li>)}</ul>
        <div className="row total"><b>Total</b><b>{money(total)}</b></div>
        {error && <p className="error-text" role="alert">{error}</p>}
        <button className="btn" disabled={busy}>{busy ? 'Placing…' : 'Place Order'}</button>
      </section>
    </form>
  )
}

export default Checkout

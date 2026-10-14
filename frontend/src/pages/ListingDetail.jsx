import {useContext, useState} from 'react'
import {Link, useNavigate, useParams} from 'react-router'
import {getErrorMessage, money} from '../api'
import {AppContext} from '../context'
import useApi from '../useApi'
import ListingCard from '../components/ListingCard'
import {ErrorBox, Loader} from '../components/ui'

const Similar = ({listing}) => {
  const {data} = useApi(`/api/listings/?category=${encodeURIComponent(listing.category)}&page_size=5`)
  const items = (data?.results || []).filter(l => l.id !== listing.id).slice(0, 4)
  return items.length ? (
    <section><h2>Similar listings</h2><div className="grid">{items.map(l => <ListingCard key={l.id} listing={l} />)}</div></section>
  ) : null
}

const ListingDetail = () => {
  const {id} = useParams()
  const navigate = useNavigate()
  const {loggedIn, addToCart} = useContext(AppContext)
  const {data: l, status, error, loading} = useApi(`/api/listings/${id}/`, [loggedIn])
  const [qty, setQty] = useState(1)
  const [msg, setMsg] = useState('')

  if (loading) return <Loader />
  if (status === 401) {
    return <ErrorBox message="This is a Senior-only deal. Log in to view it."><Link className="btn" to="/login">Log in</Link></ErrorBox>
  }
  if (error) return <ErrorBox message={status === 404 ? 'We could not find that listing.' : error} />

  const onAdd = async () => {
    if (!loggedIn) return navigate('/login')
    const res = await addToCart(l.id, qty)
    setMsg(res.ok ? 'Added to your cart.' : getErrorMessage(await res.json().catch(() => null)))
  }

  return (
    <>
      <div className="detail">
        <img src={l.imageUrl} alt={l.title} />
        <div>
          {l.is_senior_deal && <span className="tag senior">Senior-only deal</span>}
          <h1>{l.title}</h1>
          <p className="muted">{l.hostel} · {l.condition} · sold by {l.seller_name}</p>
          <p className="price">{money(Number(l.price))} {l.negotiable && <span className="tag">Negotiable</span>}</p>
          <p>Rating {l.rating} ({l.total_reviews} reviews) · <b>{l.availability}</b></p>
          <p>{l.description}</p>
          <div className="row gap">
            <input type="number" min="1" value={qty} onChange={e => setQty(Math.max(1, Number(e.target.value)))} aria-label="Quantity" className="qty" />
            <button type="button" className="btn" onClick={onAdd} disabled={l.availability !== 'Available'}>ADD TO CART</button>
          </div>
          {msg && <p role="status" className="muted">{msg}</p>}
        </div>
      </div>
      <Similar listing={l} />
    </>
  )
}

export default ListingDetail

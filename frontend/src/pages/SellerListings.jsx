import {useState} from 'react'
import {Link} from 'react-router'
import {apiFetch, money} from '../api'
import useApi from '../useApi'
import {ErrorBox, Loader, Pagination} from '../components/ui'

export const SellerOnly = ({status, error}) =>
  status === 403 ? <ErrorBox message="Only seller accounts can open this screen. Create a seller account to start selling." /> : <ErrorBox message={error} />

const SellerListings = () => {
  const [page, setPage] = useState(1)
  const [typing, setTyping] = useState('')
  const [search, setSearch] = useState('')
  const [tick, setTick] = useState(0)
  const {data, status, error, loading} = useApi(`/api/seller/listings/?page=${page}&search=${encodeURIComponent(search)}`, [tick])

  const onDelete = async l => {
    if (!window.confirm(`Delete "${l.title}"?`)) return
    const res = await apiFetch(`/api/listings/${l.id}/`, {method: 'DELETE'}) // 204, no body
    if (res.status === 204) setTick(tick + 1)
  }
  const onSearch = e => {
    e.preventDefault()
    setPage(1)
    setSearch(typing.trim())
  }

  return (
    <>
      <div className="row"><h1 className="grow">My listings</h1><Link className="btn" to="/seller/listings/new">Add Listing</Link></div>
      <nav className="subnav"><Link to="/seller">Dashboard</Link><Link to="/seller/orders">Seller orders</Link></nav>
      <form onSubmit={onSearch} className="search"><input value={typing} onChange={e => setTyping(e.target.value)} placeholder="Search your listings" aria-label="Search" /><button className="btn">Search</button></form>
      {loading ? <Loader /> : error ? <SellerOnly status={status} error={error} /> : data.results.length === 0 ? (
        <div className="empty"><h3>No listings yet</h3><p className="muted">Add your first listing to start selling.</p></div>
      ) : (
        <>
          <ul className="rows">
            {data.results.map(l => (
              <li key={l.id} className="row-item">
                <img src={l.image_url} alt="" />
                <div className="grow"><b>{l.title}</b><p className="muted">{l.category} · {l.availability}{l.is_senior_deal ? ' · Senior-only' : ''}</p></div>
                <strong>{money(Number(l.price))}</strong>
                <Link className="btn ghost" to={`/seller/listings/${l.id}/edit`}>Edit</Link>
                <button type="button" className="btn danger" onClick={() => onDelete(l)}>Delete</button>
              </li>
            ))}
          </ul>
          <Pagination page={page} totalPages={data.total_pages} onChange={setPage} />
        </>
      )}
    </>
  )
}

export default SellerListings

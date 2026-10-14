import {useState} from 'react'
import {Link} from 'react-router'
import {apiFetch, money} from '../api'
import useApi from '../useApi'
import {Loader, Pagination, StatusBadge} from '../components/ui'
import {SellerOnly} from './SellerListings'

const NEXT_LABEL = {placed: 'Mark shipped', shipped: 'Mark delivered'}

const SellerOrders = () => {
  const [page, setPage] = useState(1)
  const [tick, setTick] = useState(0)
  const {data, status, error, loading} = useApi(`/api/seller/orders/?page=${page}`, [tick])

  const advance = async row => {
    const res = await apiFetch(`/api/seller/orders/${row.id}/advance/`, {method: 'PATCH'})
    if (res.ok) setTick(tick + 1)
  }
  if (loading) return <Loader />
  if (error) return <SellerOnly status={status} error={error} />
  return (
    <>
      <h1>Seller orders</h1>
      <nav className="subnav"><Link to="/seller">Dashboard</Link><Link to="/seller/listings">My listings</Link></nav>
      {data.results.length === 0 ? <div className="empty"><h3>No orders yet</h3><p className="muted">Orders containing your listings show up here.</p></div> : (
        <ul className="rows">
          {data.results.map(r => (
            <li key={r.id} className="row-item">
              <div className="grow"><b>{r.title}</b><p className="muted">Order #{r.order} · {r.buyer} · meet at {r.meetup_point} · qty {r.quantity}</p></div>
              <strong>{money(Number(r.amount))}</strong>
              <StatusBadge status={r.status} />
              {NEXT_LABEL[r.status] && <button type="button" className="btn" onClick={() => advance(r)}>{NEXT_LABEL[r.status]}</button>}
            </li>
          ))}
        </ul>
      )}
      <Pagination page={page} totalPages={data.total_pages} onChange={setPage} />
    </>
  )
}

export default SellerOrders

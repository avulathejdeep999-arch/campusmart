import {useState} from 'react'
import {Link} from 'react-router'
import {money} from '../api'
import useApi from '../useApi'
import {ErrorBox, Loader, Pagination, StatusBadge} from '../components/ui'

const Orders = () => {
  const [page, setPage] = useState(1)
  const {data, error, loading} = useApi(`/api/orders/?page=${page}`)
  if (loading) return <Loader />
  if (error) return <ErrorBox message={error} />
  if (data.count === 0) return <div className="empty"><h2>No orders yet</h2><Link className="btn" to="/listings">Browse listings</Link></div>
  return (
    <>
      <h1>My orders</h1>
      <div className="stack">
        {data.results.map(o => (
          <article key={o.id} className="panel row">
            <div className="grow">
              <h3>Order #{o.id}</h3>
              <p className="muted">{new Date(o.created_at).toLocaleDateString()} · {o.total_items} items</p>
            </div>
            <StatusBadge status={o.status} />
            <strong>{money(Number(o.total_price))}</strong>
            <Link className="btn ghost" to={`/orders/${o.id}`}>View Details</Link>
          </article>
        ))}
      </div>
      <Pagination page={page} totalPages={data.total_pages} onChange={setPage} />
    </>
  )
}

export default Orders

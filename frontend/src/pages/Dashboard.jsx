import {Link} from 'react-router'
import {money} from '../api'
import useApi from '../useApi'
import {Loader, StatusBadge} from '../components/ui'
import {SellerOnly} from './SellerListings'

const Dashboard = () => {
  const {data: d, status, error, loading} = useApi('/api/seller/dashboard/')
  if (loading) return <Loader />
  if (error) return <SellerOnly status={status} error={error} />
  const max = Math.max(1, ...d.last_7_days.map(x => Number(x.revenue)))
  return (
    <>
      <h1>Seller dashboard</h1>
      <nav className="subnav"><Link to="/seller/listings">My listings</Link><Link to="/seller/orders">Seller orders</Link></nav>
      <div className="stats">
        <div className="panel"><p className="muted">Listings</p><b>{d.total_listings}</b></div>
        <div className="panel"><p className="muted">Orders</p><b>{d.total_orders}</b></div>
        <div className="panel"><p className="muted">Items sold</p><b>{d.items_sold}</b></div>
        <div className="panel"><p className="muted">Revenue</p><b>{money(Number(d.revenue))}</b></div>
      </div>
      <div className="banner">{d.to_hand_over > 0 ? `${d.to_hand_over} item(s) still to hand over.` : 'Nothing waiting to be handed over.'}</div>
      <section className="panel">
        <h3>Last 7 days</h3>
        <div className="chart" role="img" aria-label="Revenue for the last seven days">
          {d.last_7_days.map(x => (
            <div key={x.date} className="bar-col">
              <span className="bar-val">{Number(x.revenue) > 0 ? money(Number(x.revenue)) : ''}</span>
              <div className="bar" style={{height: `${(Number(x.revenue) / max) * 100}%`}} />
              <span className="muted">{new Date(x.date).toLocaleDateString(undefined, {weekday: 'short'})}</span>
            </div>
          ))}
        </div>
      </section>
      <div className="two">
        <section className="panel"><h3>Top listings</h3>
          {d.top_listings.length === 0 ? <p className="muted">No sales yet.</p> : <ul className="plain">{d.top_listings.map(t => <li key={t.title} className="row"><span>{t.title} ({t.quantity})</span><b>{money(Number(t.revenue))}</b></li>)}</ul>}
        </section>
        <section className="panel"><h3>Items by status</h3>
          <ul className="plain">{Object.entries(d.items_by_status).map(([s, n]) => <li key={s} className="row"><StatusBadge status={s} /><b>{n}</b></li>)}</ul>
        </section>
      </div>
    </>
  )
}

export default Dashboard

import {useState} from 'react'
import {useParams} from 'react-router'
import {apiFetch, getErrorMessage, money} from '../api'
import useApi from '../useApi'
import {ErrorBox, Loader, StatusBadge} from '../components/ui'

const OrderDetail = () => {
  const {id} = useParams()
  const [tick, setTick] = useState(0)
  const {data: o, status, error, loading} = useApi(`/api/orders/${id}/`, [tick])
  const [msg, setMsg] = useState('')

  if (loading) return <Loader />
  if (error) return <ErrorBox message={status === 404 ? 'We could not find that order.' : error} />

  const cancel = async () => {
    const res = await apiFetch(`/api/orders/${id}/cancel/`, {method: 'POST'})
    if (res.ok) setTick(tick + 1)
    else setMsg(getErrorMessage(await res.json().catch(() => null)))
  }
  const a = o.address
  return (
    <>
      <div className="row"><h1 className="grow">Order #{o.id}</h1><StatusBadge status={o.status} /></div>
      <ul className="rows">
        {o.items.map(i => (
          <li key={i.id} className="row-item">
            <img src={i.image_url} alt="" />
            <div className="grow"><b>{i.title}</b><p className="muted">{i.hostel} · {i.condition} · {i.quantity} × {money(Number(i.price))}</p></div>
            <StatusBadge status={i.status} /><strong>{money(Number(i.amount))}</strong>
          </li>
        ))}
      </ul>
      <div className="two">
        <section className="panel"><h3>Delivery</h3><p>{a.full_name}, {a.phone}<br />{a.address}, {a.city}, {a.state} {a.pincode}</p><p>Meetup point: <b>{o.meetup_point_label}</b></p></section>
        <section className="panel"><h3>Payment</h3><p>{o.payment_method === 'COD' ? 'Cash at Meetup' : 'Paid online'} · {o.is_paid ? 'Paid' : 'Not paid yet'}</p><p>Total <b>{money(Number(o.total_price))}</b></p></section>
      </div>
      {o.can_cancel && <button type="button" className="btn danger" onClick={cancel}>Cancel order</button>}
      {msg && <p className="error-text" role="alert">{msg}</p>}
    </>
  )
}

export default OrderDetail

import {useEffect, useState} from 'react'
import {useNavigate, useParams} from 'react-router'
import {apiFetch, getErrorMessage} from '../api'
import useApi from '../useApi'
import {Loader} from '../components/ui'

const EMPTY = {title: '', hostel: '', condition: 'Good', negotiable: 'false', category: 'Books', price: '', imageUrl: '', availability: 'Available', description: '', is_senior_deal: 'false'}

const ListingForm = () => {
  const {id} = useParams()
  const editing = Boolean(id)
  const navigate = useNavigate()
  const {data, loading} = useApi(editing ? `/api/listings/${id}/` : null)
  const [form, setForm] = useState(EMPTY)
  const [error, setError] = useState('')
  const [busy, setBusy] = useState(false)

  useEffect(() => {
    if (data) setForm({...data, price: String(data.price), negotiable: String(data.negotiable), is_senior_deal: String(data.is_senior_deal)})
  }, [data])

  if (editing && loading) return <Loader />
  const set = k => e => setForm({...form, [k]: e.target.value})

  const onSubmit = async e => {
    e.preventDefault()
    setBusy(true)
    setError('')
    const body = {
      title: form.title, hostel: form.hostel, condition: form.condition, category: form.category, price: form.price,
      imageUrl: form.imageUrl, availability: form.availability, description: form.description,
      negotiable: form.negotiable === 'true', is_senior_deal: form.is_senior_deal === 'true',
    }
    const res = await apiFetch(editing ? `/api/listings/${id}/` : '/api/listings/', {method: editing ? 'PATCH' : 'POST', body: JSON.stringify(body)})
    if (res.ok) navigate('/seller/listings')
    else {
      setError(res.status === 403 ? 'Only the seller who owns this listing can change it.' : getErrorMessage(await res.json().catch(() => null)))
      setBusy(false)
    }
  }
  const yn = k => (
    <select value={form[k]} onChange={set(k)}><option value="true">Yes</option><option value="false">No</option></select>
  )

  return (
    <form className="panel narrow" onSubmit={onSubmit}>
      <h1>{editing ? 'Edit listing' : 'Add listing'}</h1>
      <label>Title<input value={form.title} onChange={set('title')} required /></label>
      <label>Hostel<input value={form.hostel} onChange={set('hostel')} placeholder="Hostel C" required /></label>
      <label>Condition<select value={form.condition} onChange={set('condition')}>{['Like New', 'Good', 'Fair'].map(c => <option key={c}>{c}</option>)}</select></label>
      <label>Negotiable {yn('negotiable')}</label>
      <label>Category<select value={form.category} onChange={set('category')}>{['Books', 'Electronics', 'Hostel Essentials', 'Cycles', 'Sports'].map(c => <option key={c}>{c}</option>)}</select></label>
      <label>Price (₹)<input type="number" min="1" step="0.01" value={form.price} onChange={set('price')} required /></label>
      <label>Image address<input value={form.imageUrl} onChange={set('imageUrl')} placeholder="https://…" /></label>
      <label>Availability<select value={form.availability} onChange={set('availability')}><option>Available</option><option>Sold</option></select></label>
      <label>Description<textarea rows="3" value={form.description} onChange={set('description')} /></label>
      <label>Senior-only deal {yn('is_senior_deal')}</label>
      {error && <p className="error-text" role="alert">{error}</p>}
      <button className="btn" disabled={busy}>{busy ? 'Saving…' : 'Save'}</button>
    </form>
  )
}

export default ListingForm

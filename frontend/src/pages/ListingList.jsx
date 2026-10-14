import {useContext, useState} from 'react'
import {Link, useSearchParams} from 'react-router'
import {AppContext} from '../context'
import useApi from '../useApi'
import ListingCard from '../components/ListingCard'
import {ErrorBox, Loader, Pagination} from '../components/ui'

const CATEGORIES = ['Books', 'Electronics', 'Hostel Essentials', 'Cycles', 'Sports']
const HOSTELS = ['Hostel A', 'Hostel B', 'Hostel C', 'Hostel D']
const RATINGS = [4, 3, 2, 1]
const SORTS = [
  {value: '', label: 'Newest listed'},
  {value: 'price', label: 'Price: Low to High'},
  {value: '-price', label: 'Price: High to Low'},
  {value: '-rating', label: 'Top rated'},
]

const SeniorStrip = () => {
  const {loggedIn} = useContext(AppContext)
  const {data, status, loading} = useApi('/api/listings/?is_senior_deal=true&page_size=6', [loggedIn])
  return (
    <section className="strip">
      <h2>Senior-only deals</h2>
      {loading ? <Loader /> : status === 401 ? (
        <div className="banner">Final-year seniors sell cheap, but only to signed-in members. <Link to="/login">Log in</Link> to see 6 deals.</div>
      ) : (
        <div className="grid">{data?.results.map(l => <ListingCard key={l.id} listing={l} />)}</div>
      )}
    </section>
  )
}

const ListingList = () => {
  const [params, setParams] = useSearchParams()
  const category = params.get('category') || ''
  const hostel = params.get('hostel') || ''
  const rating = params.get('rating') || ''
  const ordering = params.get('ordering') || ''
  const search = params.get('search') || ''
  const page = Number(params.get('page') || 1)
  const [typing, setTyping] = useState(search) // what is being typed ...

  const update = patch => {
    const next = new URLSearchParams(params)
    Object.entries({page: '1', ...patch}).forEach(([k, v]) => (v ? next.set(k, v) : next.delete(k)))
    setParams(next)
  }
  const onSearch = e => {
    e.preventDefault()
    update({search: typing.trim()}) // ... and what was submitted: typing sends no requests, Enter sends one
  }

  const q = new URLSearchParams()
  if (category) q.set('category', category) // the WORD, not a number
  if (hostel) q.set('hostel', hostel)
  if (rating) q.set('rating', rating)
  if (ordering) q.set('ordering', ordering)
  if (search) q.set('search', search)
  q.set('page', page)
  const {data, error, loading} = useApi(`/api/listings/?${q}`)

  const radio = (name, value, label, current) => (
    <label key={value} className="opt">
      <input type="radio" name={name} checked={current === String(value)} onChange={() => update({[name]: String(value)})} /> {label}
    </label>
  )

  return (
    <>
      <SeniorStrip />
      <div className="layout">
        <aside className="filters">
          <h3>Category</h3>
          {radio('category', '', 'All', category)}
          {CATEGORIES.map(c => radio('category', c, c, category))}
          <h3>Hostel</h3>
          {radio('hostel', '', 'Any', hostel)}
          {HOSTELS.map(h => radio('hostel', h, h, hostel))}
          <h3>Rating</h3>
          {radio('rating', '', 'Any', rating)}
          {RATINGS.map(r => radio('rating', r, `${r} & up`, rating))}
          <button type="button" className="btn ghost" onClick={() => {setTyping(''); setParams({})}}>Clear filters</button>
        </aside>
        <section>
          <div className="toolbar">
            <form onSubmit={onSearch} className="search">
              <input value={typing} onChange={e => setTyping(e.target.value)} placeholder="Search title or hostel" aria-label="Search" />
              <button className="btn">Search</button>
            </form>
            <select value={ordering} onChange={e => update({ordering: e.target.value})} aria-label="Sort">
              {SORTS.map(s => <option key={s.value} value={s.value}>{s.label}</option>)}
            </select>
          </div>
          {loading ? <Loader /> : error ? <ErrorBox message={error} /> : data.results.length === 0 ? (
            <div className="empty"><h3>No listings found</h3><p className="muted">Nothing matches these filters yet. Try clearing a filter.</p></div>
          ) : (
            <>
              <p className="muted">{data.count} listings</p>
              <div className="grid">{data.results.map(l => <ListingCard key={l.id} listing={l} />)}</div>
              <Pagination page={page} totalPages={data.total_pages} onChange={p => update({page: String(p)})} />
            </>
          )}
        </section>
      </div>
    </>
  )
}

export default ListingList

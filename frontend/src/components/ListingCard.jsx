import {Link} from 'react-router'
import {FiStar} from 'react-icons/fi'
import {money} from '../api'

const ListingCard = ({listing}) => (
  <Link to={`/listings/${listing.id}`} className="card listing-card">
    <img src={listing.imageUrl} alt={listing.title} loading="lazy" />
    <div className="card-body">
      {listing.is_senior_deal && <span className="tag senior">Senior-only deal</span>}
      <h3>{listing.title}</h3>
      <p className="muted">{listing.hostel} · {listing.condition}</p>
      <div className="row">
        <strong>{money(Number(listing.price))}</strong>
        <span className="muted"><FiStar /> {listing.rating}</span>
      </div>
      {listing.negotiable && <span className="tag">Negotiable</span>}
    </div>
  </Link>
)

export default ListingCard

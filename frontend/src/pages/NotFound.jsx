import {Link} from 'react-router'

const NotFound = () => (
  <div className="center col">
    <h1>Page not found</h1>
    <p className="muted">That address does not lead anywhere on CampusMart.</p>
    <Link to="/" className="btn">Go home</Link>
  </div>
)

export default NotFound

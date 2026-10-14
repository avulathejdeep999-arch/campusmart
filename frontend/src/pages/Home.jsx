import {Link} from 'react-router'

const CATEGORIES = ['Books', 'Electronics', 'Hostel Essentials', 'Cycles', 'Sports']

const Home = () => (
  <section className="hero">
    <h1>Buy and sell on campus, hand to hand.</h1>
    <p>Calculators, cycles and course books from students who already finished the semester. Meet at the Main Gate, the Library Steps or the Canteen.</p>
    <div className="row gap">
      <Link to="/listings" className="btn">Browse listings</Link>
      <Link to="/seller/listings/new" className="btn ghost">Sell something</Link>
    </div>
    <div className="chips">
      {CATEGORIES.map(c => (
        <Link key={c} to={`/listings?category=${encodeURIComponent(c)}`} className="chip">{c}</Link>
      ))}
    </div>
  </section>
)

export default Home

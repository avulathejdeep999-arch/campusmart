import {useCallback, useEffect, useMemo, useState} from 'react'
import {Route, Routes} from 'react-router'
import {apiFetch, clearTokens, getAccessToken, getRefreshToken, saveTokens} from './api'
import {AppContext} from './context'
import Header from './components/Header'
import ProtectedRoute from './components/ProtectedRoute'
import Home from './pages/Home'
import Login from './pages/Login'
import Register from './pages/Register'
import ListingList from './pages/ListingList'
import ListingDetail from './pages/ListingDetail'
import Cart from './pages/Cart'
import Checkout from './pages/Checkout'
import Orders from './pages/Orders'
import OrderDetail from './pages/OrderDetail'
import Dashboard from './pages/Dashboard'
import SellerListings from './pages/SellerListings'
import ListingForm from './pages/ListingForm'
import SellerOrders from './pages/SellerOrders'
import NotFound from './pages/NotFound'

// The cart row has TWO ids: `id` is the row (PATCH/DELETE), `listingId` is the listing (POST add).
// Keep them apart the moment data enters React, and turn money text into a number once.
const formatCartItem = item => ({
  id: item.id,
  listingId: item.listing,
  title: item.listing_title,
  condition: item.listing_condition,
  price: Number(item.listing_price),
  image: item.listing_image,
  quantity: item.quantity,
})

const App = () => {
  const [loggedIn, setLoggedIn] = useState(Boolean(getAccessToken()))
  const [cartItems, setCartItems] = useState([])

  const getCart = useCallback(async () => {
    if (getAccessToken() === undefined) {
      setCartItems([])
      return
    }
    const res = await apiFetch('/api/cart/')
    if (res.ok) setCartItems((await res.json()).items.map(formatCartItem))
  }, [])

  useEffect(() => {
    getCart()
  }, [loggedIn, getCart])

  const login = tokens => {
    saveTokens(tokens)
    setLoggedIn(true)
  }

  const logout = async () => {
    // Tell the server first (it blacklists the refresh token -> 205), clear cookies only after the answer.
    try {
      await apiFetch('/api/users/logout/', {method: 'POST', body: JSON.stringify({refresh: getRefreshToken()})})
    } finally {
      clearTokens()
      setCartItems([])
      setLoggedIn(false)
    }
  }

  const addToCart = async (listingId, quantity = 1) => {
    const res = await apiFetch('/api/cart/add/', {method: 'POST', body: JSON.stringify({listing: listingId, quantity})})
    await getCart()
    return res
  }
  const removeCartItem = async rowId => {
    await apiFetch(`/api/cart/items/${rowId}/`, {method: 'DELETE'})
    await getCart()
  }
  const updateCartItem = async (rowId, quantity) => {
    if (quantity < 1) return removeCartItem(rowId)
    await apiFetch(`/api/cart/items/${rowId}/`, {method: 'PATCH', body: JSON.stringify({quantity})}) // SETS quantity
    return getCart()
  }

  const value = useMemo(
    () => ({loggedIn, login, logout, cartItems, getCart, addToCart, removeCartItem, updateCartItem}),
    // eslint-disable-next-line react-hooks/exhaustive-deps
    [loggedIn, cartItems],
  )

  return (
    <AppContext.Provider value={value}>
      <Header />
      <main className="page">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/listings" element={<ListingList />} />
          <Route path="/listings/:id" element={<ListingDetail />} />
          <Route element={<ProtectedRoute />}>
            <Route path="/cart" element={<Cart />} />
            <Route path="/checkout" element={<Checkout />} />
            <Route path="/orders" element={<Orders />} />
            <Route path="/orders/:id" element={<OrderDetail />} />
            <Route path="/seller" element={<Dashboard />} />
            <Route path="/seller/listings" element={<SellerListings />} />
            <Route path="/seller/listings/new" element={<ListingForm />} />
            <Route path="/seller/listings/:id/edit" element={<ListingForm />} />
            <Route path="/seller/orders" element={<SellerOrders />} />
          </Route>
          <Route path="*" element={<NotFound />} />
        </Routes>
      </main>
    </AppContext.Provider>
  )
}

export default App

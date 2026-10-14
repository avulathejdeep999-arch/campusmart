import {ClipLoader} from 'react-spinners'

export const Loader = () => (
  <div className="center" data-testid="loader"><ClipLoader color="#0e7c7b" size={36} /></div>
)

export const ErrorBox = ({message, children}) => (
  <div className="error-box" role="alert"><p>{message}</p>{children}</div>
)

export const StatusBadge = ({status}) => <span className={`status ${status}`}>{status}</span>

export const Pagination = ({page, totalPages, onChange}) =>
  totalPages > 1 ? (
    <div className="pager">
      <button type="button" className="btn ghost" disabled={page <= 1} onClick={() => onChange(page - 1)}>Previous</button>
      <span>Page {page} of {totalPages}</span>
      <button type="button" className="btn ghost" disabled={page >= totalPages} onClick={() => onChange(page + 1)}>Next</button>
    </div>
  ) : null

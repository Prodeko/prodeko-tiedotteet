import {CALL_API} from 'redux-api-middleware'
import {addToStorage, removeFromStorage} from '../../util/localStorage'

// Initial state
const initialState = {
  isFetching: false,
  error: null,
  data: []
}

// Actions
export const REQUEST_CONTENT = 'CONTENT/REQUEST_CONTENT'
export const REQUEST_CONTENT_SUCCESS = 'CONTENT/REQUEST_CONTENT_SUCCESS'
export const REQUEST_CONTENT_FAILURE = 'CONTENT/REQUEST_CONTENT_FAILURE'

export const MARK_READ = 'CONTENT/MARK_READ'
export const MARK_UNREAD = 'CONTENT/MARK_UNREAD'

export const markRead = (payload) => {
  addToStorage(payload)
  return {
    type: MARK_READ,
    payload
  }
}

export const markUnRead = (payload) => {
  removeFromStorage(payload)
  return {
    type: MARK_UNREAD,
    payload
  }
}

export const fetchContent = () => {
  return {
    [CALL_API]: {
      endpoint: (process.env.NODE_ENV === 'production' ? '' : 'https://tiedotteet.prodeko.org') + '/api/content/',
      credentials: "same-origin",
      headers: {
        "X-CSRFToken": window.csrfToken,
        "Accept": "application/json",
        "Content-Type": "application/json"
      },
      method: 'get',
      types: [REQUEST_CONTENT, REQUEST_CONTENT_SUCCESS, REQUEST_CONTENT_FAILURE]
    }
  }
}

// Reducer
export const ContentStateReducer = (state = initialState, action = {}) => {
  switch (action.type) {
    case REQUEST_CONTENT:
      return {
        ...state,
        isFetching: true,
        error: null
      }
    case REQUEST_CONTENT_SUCCESS:
      return {
        ...state,
        isFetching: false,
        error: null,
        data: action.payload
      }
    case REQUEST_CONTENT_FAILURE:
      return {
        ...state,
        isFetching: false,
        error: action.payload
      }
    default:
      return state
  }
}

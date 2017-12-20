import React, { Component } from 'react'
import PropTypes from 'prop-types'

class LoginForm extends Component {
  render() {
    return (
      <div className="auth-form">
        <form method="post" action="/login/">
          <input type="hidden" name="csrfmiddlewaretoken" value={window.csrfToken}/>
          <input type="hidden" name="next" value="/"/>
          <input type="username" name="username"/>
          <input type="password" name="password"/>
          <button type="submit">Login</button>
        </form>
      </div>
    )
  }
}

LoginForm.propTypes = {

}

export default LoginForm

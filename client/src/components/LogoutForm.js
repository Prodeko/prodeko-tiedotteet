import React, { Component } from 'react'
import PropTypes from 'prop-types'

class LogoutForm extends Component {
  render() {
    return (
      <div id="logout-form">
        <form method="get" action="/logout/">
          <input type="hidden" name="next" value="/"/>
          <input type="submit" value ="Logout"/>
        </form>
      </div>
    )
  }
}

LogoutForm.propTypes = {
}

export default LogoutForm

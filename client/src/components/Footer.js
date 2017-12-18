import React, { Component } from 'react'
import PropTypes from 'prop-types'

class Footer extends Component {
  render() {
    return (
      <div id="footer">
        <img src={"/public/assets/prodeko.png"} alt="Prodeko"/>
      </div>
    )
  }
}

Footer.propTypes = {

}

export default Footer

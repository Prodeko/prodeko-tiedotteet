import React, { Component } from 'react'
import PropTypes from 'prop-types'

class Footer extends Component {
  render() {
    return (
      <div id="footer">
        <img src={"/public/assets/prodeko.png"} alt="Prodeko"/>
        <hr/>
        <span><a href="https://www.prodeko.org/tietosuojakaytanto/">Prodekon tietosuojakäytäntö</a></span>
      </div>
    )
  }
}

Footer.propTypes = {

}

export default Footer

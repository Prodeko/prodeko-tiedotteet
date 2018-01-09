import React, { Component } from 'react'
import PropTypes from 'prop-types'

class TableOfContents extends Component {

  handleClick = (messageId) => {
    this.props.sendAnalyticsEvent('Table of Contents', 'click', null, messageId)
  }

  render() {
    return (
      <div id="table-of-contents">
        {this.props.content.data.map((category, key) =>  category.messages.length > 0 ? (
          <ul key={key} className="main-list">
            <li className="category-title">{category.title}</li>
            <ul className="sub-list">
              {category.messages.map((message, key) => (
                <li key={key} className="message-title">
                  <a href={`#${message.id}`} onClick={() => this.handleClick(message.id)}>{message.header}</a>
                </li>
              ))}
            </ul>
          </ul>

        ) : null)}
        <hr/>
      </div>
    )
  }
}

TableOfContents.propTypes = {
  content: PropTypes.object.isRequired,
  sendAnalyticsEvent: PropTypes.func.isRequired
}

export default TableOfContents
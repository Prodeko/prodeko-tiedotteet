import React, { Component } from 'react'
import PropTypes from 'prop-types'

class TableOfContents extends Component {
  render() {
    return (
      <div id="table-of-contents">
        <div>
          {this.props.content.data.map((category, key) =>  category.messages.length > 0 ? (
            <div key={key}>
              <span>{category.title}</span>
              <ul>
                {category.messages.map((message, key) => (
                  <li key={key}>{message.header}</li>
                ))}
              </ul>
            </div>

          ) : null)}
        </div>
      </div>
    )
  }
}

TableOfContents.propTypes = {
  content: PropTypes.object.isRequired
}

export default TableOfContents
import React, { Component } from 'react'
import PropTypes from 'prop-types'

class TableOfContents extends Component {
  render() {
    return (
      <div id="table-of-contents">
        {this.props.content.data.map((category, key) =>  category.messages.length > 0 ? (
          <ul key={key}>
            <li className="category-title">{category.title}</li>
            <ul>
              {category.messages.map((message, key) => (
                <li key={key} className="message-title"><a href={`#${message.id}`}>{message.header}</a></li>
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
  content: PropTypes.object.isRequired
}

export default TableOfContents
import React, { Component } from 'react'
import PropTypes from 'prop-types'

class SideListItem extends Component {
  render() {
    return (
      <li className={`sidebar-list-item ${this.props.isRead ? 'read' : ''} ${this.props.isNew ? 'new' : ''}`}>
        <a htmlFor={this.props.id} href={`#${this.props.id}`}>
          <div className="icon-container">
            {this.props.isNew &&
              <span>New</span>
            }
          </div>
          <div className="text-container">
            {this.props.text}
          </div>
        </a>
      </li>
    )
  }
}

SideListItem.propTypes = {
  id: PropTypes.number.isRequired,
  isRead: PropTypes.bool.isRequired,
  text: PropTypes.string.isRequired,
  isNew: PropTypes.bool.isRequired
}

export default SideListItem

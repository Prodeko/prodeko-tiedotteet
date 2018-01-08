import React, { Component } from 'react'
import PropTypes from 'prop-types'
import Moment from 'moment'

class SideListItem extends Component {
  render() {
    return (
      <li className={`sidebar-list-item ${this.props.isRead ? 'read' : ''} ${this.props.isNew ? 'new' : ''}`}>
        <a htmlFor={this.props.id} href={`#${this.props.id}`}>
          {this.props.isNew &&
            <div className="icon-container text-red">
              <span>New</span>
            </div>
          }
          {this.props.showDeadline &&
          <div className="icon-container text-light-grey">
            <span>DL: {Moment(this.props.deadlineDate).format("D.M.Y")}</span>
          </div>
          }
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
  isNew: PropTypes.bool.isRequired,
  showDeadline: PropTypes.bool.isRequired,
  deadlineDate: PropTypes.string.isRequired
}

export default SideListItem

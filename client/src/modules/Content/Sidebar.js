import React, { Component } from 'react'
import PropTypes from 'prop-types'
import SideListItem from '../../components/SideListItem'
import {isInStore} from '../../util/localStorage'

class Sidebar extends Component {
  isNew = (pubDate) => {
    const today = new Date()
    const date = new Date(pubDate)
    const diff = Math.round((today-date)/(1000*60*60*24))
    return diff < 3
  }
  render() {
    return (
      <aside id="sidebar" className={this.props.additionalClasses}>
        <div id="sidebar-content">
        {this.props.content.data.filter(c => c.messages.length > 0).map((d, key) => (
          <div key={key}>
            <span className="sidebar-category">{d.title}</span>
            <ul className="sidebar-list">
              {d.messages.map((m,key) => (
                <SideListItem
                  key={key}
                  id={m.id}
                  text={m.header}
                  isRead={isInStore(m.id)}
                  isNew={this.isNew(m.pub_date)}
                />
              ))}
            </ul>
          </div>
        ))}
        </div>
      </aside>
    )
  }
}

Sidebar.propTypes = {
  content: PropTypes.object.isRequired,
  markRead: PropTypes.func.isRequired,
  markUnRead: PropTypes.func.isRequired,
  additionalClasses: PropTypes.string
}

export default Sidebar

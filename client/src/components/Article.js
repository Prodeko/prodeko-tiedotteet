import React, { Component } from 'react'
import PropTypes from 'prop-types'

class Article extends Component {
  createMarkup = (htmlStr) => {
    return {__html: htmlStr}
  }
  render() {
    const {id, pubDate, dlDate, title, text} = this.props
    return (
      <div id={id} className="article">
        <span className="pub-date">Published {pubDate}</span>
        {dlDate &&
          <span className="dl-date">Deadline {dlDate}</span>
        }
        <h3>{title}</h3>
        <div dangerouslySetInnerHTML={this.createMarkup(text)}/>
        <hr/>
      </div>
    )
  }
}

Article.propTypes = {
  id: PropTypes.number.isRequired,
  pubDate: PropTypes.string.isRequired,
  dlDate: PropTypes.string,
  title: PropTypes.string.isRequired,
  text: PropTypes.string.isRequired
}

export default Article

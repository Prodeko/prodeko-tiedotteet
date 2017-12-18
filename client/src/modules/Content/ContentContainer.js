import {bindActionCreators} from 'redux';
import {connect} from 'react-redux'
import * as ContentStateActions from './ContentState';
import ContentView from './ContentView'

export default connect(
  state => ({
    content: state.content
  }),
  dispatch => {
    return {
      Contentactions: bindActionCreators(ContentStateActions, dispatch)
    }
  }
)(ContentView)

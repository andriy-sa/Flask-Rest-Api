import React from 'react'
import {debounce} from 'lodash'
import api from '../../Api'
import ReactDOM from 'react-dom';
import {Link} from 'react-router'

class Autocomplete extends React.Component {

  constructor(props) {
    super(props);

    this.state = {
      q: '',
      results: [],
      showResults: false
    };

    this.debounceGetSuggestions = debounce(this.autocomplete, 350)
  }

  componentDidMount() {
    document.addEventListener('click', this.handleClickOutside.bind(this), true);
  }

  componentWillUnmount() {
    document.removeEventListener('click', this.handleClickOutside.bind(this), true);
  }

  handleClickOutside(event) {
    const domNode = ReactDOM.findDOMNode(this);

    if ((!domNode || !domNode.contains(event.target))) {
      this.setState({
        showResults: false
      });
    }
  }
  clearAutocomplete = () => {
    this.setState({
      q: '',
      results: [],
      showResults: false
    });
  };

  processAutocomplete = event => {
    let q = event.target.value;
    this.setState({q: q})
    this.debounceGetSuggestions()
  };

  autocomplete = () => {
    api.Projects.autocomplete(this.state.q).then(response => {
      if (response.status === 200) {
        this.setState({results: response.data.hits, showResults: response.data.hits.length ? true : false})
      } else {
        this.setState({results: [], showResults: false})
      }
    })
  };

  createMarkup = (item) => {
    return {__html: item.highlight.title}
  };

  render() {
    return (
      <div className="form-group autocomplete-block col-sm-4 col-sm-offset-8">
        <input type="text" onChange={this.processAutocomplete} value={this.state.q}
               className="form-control autocomplete-input" placeholder="Autocomplete"/>
        { (this.state.showResults) &&
        <div className="autocomplete-box">
          {this.state.results.map((v, i) => {
            return (
              <li key={i}>
                <Link to={`/project/${v._id}`} >
                  <span onClick={this.clearAutocomplete} dangerouslySetInnerHTML={this.createMarkup(v)}></span>
                </Link>
              </li>
            )
          })}
        </div>
        }
      </div>)
  }
}

export default Autocomplete
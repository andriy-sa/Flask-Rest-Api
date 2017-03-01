import React from 'react';
import api from '../Api'
import Pagination from 'react-js-pagination'
import classNames from 'classnames'
import {debounce} from 'lodash'
import {Link} from 'react-router'

class Projects extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      projects: [],
      totalProjects: 0,
      filter: {
        q: '',
        page: 1,
        limit:10,
        sort:'id',
        reverse:false
      }
    };

    this.debounceGetSuggestions = debounce(this.searchProjects, 350)
  }

  componentDidMount() {
    this.searchProjects()
  }

  processSearch = event => {
    const field = event.target.name;
    const filter = this.state.filter;
    filter[field] = event.target.value;
    filter['page'] = 1;
    this.setState({
      filter: filter
    });

    this.debounceGetSuggestions()
  };

  handlePageChange = pageNumber => {
    const filter = this.state.filter;
    filter['page'] = pageNumber;
    this.setState({filter: filter});
    this.searchProjects()
  };

  changeSort = sort => {
    const filter = this.state.filter;
    if (sort === filter.sort) {
      filter['reverse'] = !filter['reverse'];
    } else {
      filter['sort'] = sort;
      filter['reverse'] = false;
    }
    this.setState({
      filter: filter
    });
    this.searchProjects()
  };

  searchProjects = () => {
    api.Projects.get_list(this.state.filter).then(response => {
      if (response.status === 200) {
        this.setState({projects: response.data.data,totalProjects : response.data.count})
      } else {
        this.setState({projects: [], totalProjects: 0})
      }
    })
  };

  render() {
    return (
      <div className="projects">
        <div className="top-bar">
          <div className="col-sm-4"></div>
          <div className="col-sm-4"></div>
          <div className="col-sm-4">
            <input placeholder="Search" className="form-control" name="q" onChange={this.processSearch}
                   value={this.state.filter.q} type="text"/>
          </div>
        </div>
        <div className="table-content">
          <table className="table table-hover">
            <thead>
            <tr>
              <th onClick={() => this.changeSort('id')} className="sort">
                <span>ID </span>
                <span className={classNames({
                  'fa fa-caret-up': this.state.filter.sort === 'id' && !this.state.filter.reverse,
                  'fa fa-caret-down': this.state.filter.sort === 'id' && this.state.filter.reverse})}></span>
              </th>
              <th onClick={() => this.changeSort('title')}  className="sort">
                <span>Title </span>
                <span className={classNames({
                  'fa fa-caret-up': this.state.filter.sort === 'title' && !this.state.filter.reverse,
                  'fa fa-caret-down': this.state.filter.sort === 'title' && this.state.filter.reverse})}></span>
              </th>
              <th onClick={() => this.changeSort('company')}  className="sort">
                <span>Company </span>
                <span className={classNames({
                  'fa fa-caret-up': this.state.filter.sort === 'company' && !this.state.filter.reverse,
                  'fa fa-caret-down': this.state.filter.sort === 'company' && this.state.filter.reverse})}></span>
              </th>
              <th onClick={() => this.changeSort('price')}  className="sort">
                <span>Price </span>
                <span className={classNames({
                  'fa fa-caret-up': this.state.filter.sort === 'price' && !this.state.filter.reverse,
                  'fa fa-caret-down': this.state.filter.sort === 'price' && this.state.filter.reverse})}></span>
              </th>
              <th></th>
            </tr>
            </thead>
            <tbody>
            {this.state.projects.map((v, i) => {
              return (
                <tr key={i}>
                  <td>{v.id}</td>
                  <td>{v.title}</td>
                  <td>{v.company}</td>
                  <td>${v.price}</td>
                  <td>
										<Link to={`/project/${v.id}`} >
											More
										</Link>
                  </td>
                </tr>
              )
            })}
            </tbody>
          </table>
          { (this.state.totalProjects > this.state.filter.limit) &&
          (<Pagination
            activePage={this.state.filter.page }
            itemsCountPerPage={this.state.filter.limit}
            totalItemsCount={this.state.totalProjects}
            pageRangeDisplayed={5}
            onChange={this.handlePageChange}/>)}
        </div>
      </div>
    );
  }
}

export default Projects;
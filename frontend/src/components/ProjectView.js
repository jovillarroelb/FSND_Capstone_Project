import React, { Component } from 'react';

import '../stylesheets/App.css';
import Project from './Project';
import Search from './Search';
import $ from 'jquery';

class ProjectView extends Component {
 constructor() {
  super();
  this.state = {
   projects: [],
   page: 1,
   totalProjects: 0,
   categories: {},
   currentCategory: null,
  };
 }

 componentDidMount() {
  this.getProjects();
  this.getCategories();
 }

 getProjects = () => {
  $.ajax({
   url: `/projects?page=${this.state.page}`,
   type: 'GET',
   success: (result) => {
    this.setState({
     projects: result.projects,
     totalProjects: result.total_projects,
     categories: result.categories,
     currentCategory: result.current_category,
    });
    return;
   },
   error: (error) => {
    alert('Unable to load projects. Please try your request again');
    return;
   },
  });
 };

 getCategories = () => {
  $.ajax({
   url: `/categories`,
   type: 'GET',
   success: (result) => {
    this.setState({
     categories: result.categories,
    });
    return;
   },
   error: (error) => {
    alert('Unable to load categories. Please try your request again');
    return;
   },
  });
 };

 selectPage(num) {
  this.setState({ page: num }, () => this.getProjects());
 }

 createPagination() {
  let pageNumbers = [];
  let maxPage = Math.ceil(this.state.totalProjects / 10);
  for (let i = 1; i <= maxPage; i++) {
   pageNumbers.push(
    <span
     key={i}
     className={`page-num ${i === this.state.page ? 'active' : ''}`}
     onClick={() => {
      this.selectPage(i);
     }}
    >
     {i}
    </span>
   );
  }
  return pageNumbers;
 }

 getByCategory = (id) => {
  $.ajax({
   url: `/categories/${id}/projects`,
   type: 'GET',
   success: (result) => {
    this.setState({
     projects: result.projects,
     totalProjects: result.total_projects,
     currentCategory: result.current_category,
    });
    return;
   },
   error: (error) => {
    alert('Unable to load projects. Please try your request again');
    return;
   },
  });
 };

 submitSearch = (searchTerm) => {
  $.ajax({
   url: `/projects/search`,
   type: 'POST',
   dataType: 'json',
   contentType: 'application/json',
   data: JSON.stringify({ searchTerm: searchTerm }),
   xhrFields: {
    withCredentials: true,
   },
   crossDomain: true,
   success: (result) => {
    this.setState({
     projects: result.projects,
     totalProjects: result.total_projects,
     currentCategory: result.current_category,
    });
    return;
   },
   error: (error) => {
    alert('Unable to load projects. Please try your request again');
    return;
   },
  });
 };

 deleteAction = (id) => (action) => {
  if (action === 'DELETE') {
   if (window.confirm('are you sure you want to delete the project?')) {
    $.ajax({
     url: `/projects/${id}`,
     type: 'DELETE',
     success: (result) => {
      this.getProjects();
     },
     error: (error) => {
      alert('Unable to load projects. Please try your request again');
      return;
     },
    });
   }
  }
 };

 render() {
  return (
   <div className="project-view">
    <div className="categories-list">
     <h2
      onClick={() => {
       this.getProjects();
      }}
     >
      Categories
     </h2>
     <ul>
      {Object.keys(this.state.categories).map((id) => (
       <li
        key={id}
        onClick={() => {
         this.getByCategory(id);
        }}
       >
        {this.state.categories[id]}
        <img className="category" src={`${this.state.categories[id]}.svg`} />
       </li>
      ))}
     </ul>
     <Search submitSearch={this.submitSearch} />
    </div>
    <div className="projects-list">
     <h2>Projects</h2>
     {this.state.projects.map((p, ind) => (
      <Project
       key={p.id}
       name={p.name}
       country={p.country}
       city={p.city}
       address={p.address}
       category={this.state.categories[p.category]}
       description={p.description}
       deleteAction={this.deleteAction(p.id)}
      />
     ))}
     <div className="pagination-menu">{this.createPagination()}</div>
    </div>
   </div>
  );
 }
}

export default ProjectView;

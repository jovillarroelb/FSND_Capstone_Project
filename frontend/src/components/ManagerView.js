import React, { Component } from 'react';

import '../stylesheets/App.css';
import Manager from './Manager';
import $ from 'jquery';

class ManagerView extends Component {
 constructor() {
  super();
  this.state = {
   managers: [],
   page: 1,
   totalManagers: 0,
   categories: {},
   currentCategory: null,
  };
 }

 componentDidMount() {
  this.getManagers();
 }

 getManagers = () => {
  $.ajax({
   url: `/managers?page=${this.state.page}`,
   type: 'GET',
   success: (result) => {
    this.setState({
     managers: result.managers,
     totalManagers: result.total_managers,
    });
    return;
   },
   error: (error) => {
    alert('Unable to load managers list. Please try your request again');
    return;
   },
  });
 };

 selectPage(num) {
  this.setState({ page: num }, () => this.getManagers());
 }

 createPagination() {
  let pageNumbers = [];
  let maxPage = Math.ceil(this.state.totalManagers / 10);
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

 render() {
  return (
   <div className="manager-view">
    <div className="managers-list">
     <h2>Project Managers</h2>
     {this.state.managers.map((m, ind) => (
      <Manager
       key={m.id}
       name={m.name}
       lastname={m.lastname}
       phone={m.phone}
       email={m.email}
       //  projects={m.projects}
      />
     ))}
     <div className="pagination-menu">{this.createPagination()}</div>
    </div>
   </div>
  );
 }
}

export default ManagerView;

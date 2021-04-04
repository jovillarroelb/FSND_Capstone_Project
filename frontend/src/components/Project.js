import React, { Component } from 'react';
import '../stylesheets/Project.css';

class Project extends Component {
 constructor() {
  super();
  this.state = {
   visibleAnswer: false,
  };
 }

 render() {
  const { name, country, city, address, category, description } = this.props;
  return (
   <div className="Project-holder">
    <div className="Project-name">{name}</div>
    <div className="Project-status">
     <div className="Country">Country: {country}</div>
     <div className="City">City: {city}</div>
     <div className="Address">Address: {address}</div>
     <img className="category" src={`${category}.svg`} />
     <div className="Description">Project Description: {description}</div>
     <img
      src="delete.png"
      className="delete"
      onClick={() => this.props.deleteAction('DELETE')}
     />
    </div>
   </div>
  );
 }
}

export default Project;

import React, { Component } from 'react';
import '../stylesheets/Manager.css';

class Project extends Component {
 constructor() {
  super();
  this.state = {
   visibleAnswer: false,
  };
 }

 render() {
  const { name, lastname, phone, email, projects } = this.props;
  return (
   <div className="Manager-holder">
    <div className="Manager-name">{name}</div>
    <div className="Lastname">Lastname: {lastname}</div>
    <div className="phone">phone: {phone}</div>
    <div className="email">Email: {email}</div>
    <div className="projects">projects: {projects}</div>
    {/* <img
      src="delete.png"
      className="delete"
      onClick={() => this.props.deleteAction('DELETE')}
     /> */}
   </div>
  );
 }
}

export default Project;

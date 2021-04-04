import React, { Component } from 'react';
import $ from 'jquery';

import '../stylesheets/FormView.css';

class FormView extends Component {
 constructor(props) {
  super();
  this.state = {
   name: '',
   country: '',
   city: '',
   address: '',
   category: 1,
   description: '',
  };
 }

 componentDidMount() {
  $.ajax({
   url: `/categories`,
   type: 'GET',
   success: (result) => {
    this.setState({ categories: result.categories });
    return;
   },
   error: (error) => {
    alert('Unable to load categories. Please try your request again');
    return;
   },
  });
 }

 createProject = (event) => {
  event.preventDefault();
  $.ajax({
   url: '/projects',
   type: 'POST',
   dataType: 'json',
   contentType: 'application/json',
   data: JSON.stringify({
    name: this.state.name,
    country: this.state.country,
    city: this.state.city,
    address: this.state.address,
    category: this.state.category,
    description: this.state.description,
   }),
   xhrFields: {
    withCredentials: true,
   },
   crossDomain: true,
   success: (result) => {
    document.getElementById('add-project-form').reset(); //<<< ajustar!
    alert('Projects successfully added!');
    return;
   },
   error: (error) => {
    alert('Unable to create project. Please try your request again');
    return;
   },
  });
 };

 handleChange = (event) => {
  this.setState({ [event.target.name]: event.target.value });
 };

 render() {
  return (
   <div id="add-form">
    <h2>Create New Project</h2>
    <form
     className="form-view"
     id="add-project-form"
     onSubmit={this.createProject}
    >
     <label>
      Name
      <input type="text" name="name" onChange={this.handleChange} />
     </label>
     <label>
      Country
      <input type="text" name="country" onChange={this.handleChange} />
     </label>
     <label>
      City
      <input type="text" name="city" onChange={this.handleChange} />
     </label>
     <label>
      Address
      <input type="text" name="address" onChange={this.handleChange} />
     </label>
     {/* <label>
      Category
      <select name="category" onChange={this.handleChange}>
       {Object.keys(this.state.categories).map((id) => {
        return (
         <option key={id} value={id}>
          {this.state.categories[id]}
         </option>
        );
       })}
      </select>
     </label> */}
     <label>
      Description
      <input type="text" name="description" onChange={this.handleChange} />
     </label>
     <input type="submit" className="button" value="Create New Project" />
    </form>
   </div>
  );
 }
}

export default FormView;

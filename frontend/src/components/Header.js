import React, { Component } from 'react';
import logo from '../logo.svg';
import '../stylesheets/Header.css';

class Header extends Component {
 navTo(uri) {
  window.location.href = window.location.origin + uri;
 }

 render() {
  return (
   <div className="App-header">
    <img className="logo" src={logo} />
    <h1
     onClick={() => {
      this.navTo('');
     }}
    >
     ConstruManager v1.0
    </h1>
    <h2
     onClick={() => {
      this.navTo('');
     }}
    >
     Project List
    </h2>
    <h2
     onClick={() => {
      this.navTo('/add');
     }}
    >
     Add Project
    </h2>
    <h2
     onClick={() => {
      this.navTo('/managers');
     }}
    >
     Managers List
    </h2>
   </div>
  );
 }
}

export default Header;

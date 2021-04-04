import React, { Component } from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';

// import logo from './logo.svg';
import './stylesheets/App.css';
import FormView from './components/FormView';
import ProjectView from './components/ProjectView';
import Header from './components/Header';
import ManagerView from './components/ManagerView';

class App extends Component {
 render() {
  return (
   <div className="App">
    <Header path />
    <Router>
     <Switch>
      <Route path="/" exact component={ProjectView} />
      <Route path="/add" component={FormView} />
      <Route path="/managers" component={ManagerView} />
      <Route component={ProjectView} />
     </Switch>
    </Router>
   </div>
  );
 }
}

export default App;

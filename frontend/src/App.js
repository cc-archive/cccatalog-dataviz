import React from 'react';
import Graph2D from './components/Graph2D';
import { BrowserRouter as Router, Route } from 'react-router-dom';


function App() {
  return (
    <div className="App">
      <Router>
        <Route path='/' component={Graph2D}/>
      </Router>
    </div>
  );
}

export default App;

import React from 'react';
import './App.css';

var App = (props) => {
    const [number, setNumber] = React.useState(0);
    const [dataFrameComponent, serDataFrame] = React.useState();
    
    const handleSubmit=(event) => {
      event.preventDefault();
      let formData = new FormData();    //formdata object

      formData.append('number', number);
      console.log(formData);
      console.log(formData.keys())
      
      fetch('/dataframe', {
        method: 'POST',
        body: formData
      }).then(
        function(response) {
          if (response.status !== 200) {
            console.log('Looks like there was a problem. Status Code: ' +
              response.status);
            return;
          }
    
          // Examine the text in the response
         response.body.formData().then((data)=> console.log(data))
        }
      )
      .catch(function(err) {
        console.log('Fetch Error :-S', err);
      });
    }
  
  return (
    <div className="App">
      <header className="App-header">
      <div>My token = {window.token}</div>
      <form onSubmit={handleSubmit}>
        <label>Enter the number of Elements: </label>
        <input type="text"  name= "number" onChange={(event) => {setNumber(event.target.value)} } />
        <input type="submit" value="Submit" />

      </form>
      </header>
    </div>
  );
}

export default App;

// import logo from './logo.svg';
import './App.css';
import React, { Component } from 'react';
import PostStats from './Components/stats_post';
import PostRank from './Components/rank_post';

function App() {
  return (

    <div className="App">
      <PostStats />
      <PostRank />
      
    </div>
  );

}

// class Classifier extends React.Component {

//   state = { details: [], }

//   componentDidMount() {

//     let data;
//     axios.get("http://127.0.0.1:8000/api/tasks/")
//       .then(res => {
//         data = res.data;
//         this.setState({
//           details: data
//         });
//       })
//       .catch(err => { })
//   }

//   render() {
//     return (
//       <div>
//         <header>Data Generated From Django</header>
//         <hr></hr>
//         {this.state.details.map((output, id) => (
//           <div key={id}>
//             <h2>{output.weight}</h2>
//             <h3>{output.gender}</h3>
//             <h4>{output.age}</h4>
//           </div>
//         ) )}
//       </div>
//     )
//   }

// }

// class Classifier extends Component {
//   constructor(props) {
//       super(props)

//       this.state = {
//           weight: "",
//           gender: "",
//           age: "",

//       }
//       this.handleSubmit=this.handleSubmit.bind(this)
//   }

//   componentDidMount() {
//     this.refreshList();
//   };

//   refreshList = () => {
//     axios
//     .get("http://localhost:8000/api/tasks/")
//     .then(res => this.state({ PowerliftingClassifier: res.data}))
//     .catch(err => console.log(err))
//   }

//   handleSubmit = (event) => {
//       // pop up dialogue box with text
//       // alert(`${this.state.weight} test text`)

//       console.log(this.state);

//       this.setState({
//           weight: "",
//           gender: "",
//           age: "",
//       })

//       if (event.id) {
//         axios
//           .put('http://localhost:8000/api/tasks/${event.id}/', event)
//           .then(res => this.refreshList())
//       }
    
//   event.preventDefault()

//   }

// }

export default App;

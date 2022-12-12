import axios from 'axios'
import React, { Component } from 'react'
import './component1.css'

class PostStats extends Component {
    constructor(props) {
        super(props)

        this.state = {
            weight: "",
            gender: "",
            age: "",
            squat: "",
            bench: "",
            deadlift: "",
            squat_rank: "",
            bench_rank: "",
            deadlift_rank: ""
        }
        // this.handleSubmit=this.handleSubmit.bind(this)
    }

    weighthandler = (event) => {
        this.setState({
            weight: event.target.value
        })
    }
    genderhandler = (event) => {
        this.setState({
            gender: event.target.value
        })
    }
    agehandler = (event) => {
        this.setState({
            age: event.target.value
        })
    }
   squathandler = (event) => {
        this.setState({
            squat: event.target.value
        })
    }
    benchhandler = (event) => {
        this.setState({
            bench: event.target.value
        })
    }
    deadlifthandler = (event) => {
        this.setState({
            deadlift: event.target.value
        })
    }
    squat_rankhandler = (event) => {
        this.setState({
            squat: event.target.value
        })
    }
    bench_rankhandler = (event) => {
        this.setState({
            bench: event.target.value
        })
    }
    deadlift_rankhandler = (event) => {
        this.setState({
            deadlift: event.target.value
        })
    }


    handleSubmit = (event) => {
        // pop up dialogue box with text
        // alert(`${this.state.weight} test text`)
        event.preventDefault()
        axios
            .post("http://localhost:8000/stats/", this.state)
             .then(response => {
                console.log(response)
             })
             .catch(error =>{
                console.log(error.response)
             })
        console.log(this.state);
        this.setState({
            weight: "",
            gender: "",
            age: "",
        })


    }

    render() {
        // const {weight, gender, age} = this.state

        return (
            <div>

                <form onSubmit={this.handleSubmit }>
                    <h1>Lifting Class Registration</h1>
                    <label>weight :</label> <input type="text" value={this.state.weight} onChange={this.weighthandler} placeholder="Weight..." /><br />
                    <label>gender :</label><select onChange={this.genderhandler} defaultValue="Select Gender">
                        <option defaultValue>Select Gender</option>
                        <option value="male">Male</option>
                        <option value="female">Female</option>
                    </select><br />
                    <label>age :</label> <input type="text" value={this.state.age} onChange={this.agehandler} placeholder="Age..." /><br />
                    <label>Squat :</label> <input type="text" value={this.state.squat} onChange={this.squathandler} placeholder="Squat..." /><br />
                    <label>Bench :</label> <input type="text" value={this.state.bench} onChange={this.benchhandler} placeholder="Bench..." /><br />
                    <label>Deadlift :</label> <input type="text" value={this.state.deadlift} onChange={this.deadlifthandler} placeholder="Deadlift..." /><br />
                    <button type="submit">Submit</button>
                </form>
            </div>
        )
    }

}

export default PostStats
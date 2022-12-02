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

    handleSubmit = (event) => {
        // pop up dialogue box with text
        // alert(`${this.state.weight} test text`)
        event.preventDefault()
        axios
            .post("http://localhost:8000/api/tasks/", this.state)
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

                <form onSubmit={this.handleSubmit}>
                    <h1>Lifting Class Registration</h1>
                    <label>weight :</label> <input type="text" value={this.state.weight} onChange={this.weighthandler} placeholder="Weight..." /><br />
                    <label>gender :</label><select onChange={this.genderhandler} defaultValue="Select Gender">
                        <option defaultValue>Select Gender</option>
                        <option value="male">Male</option>
                        <option value="female">Female</option>
                    </select><br />
                    <label>age :</label> <input type="text" value={this.state.age} onChange={this.agehandler} placeholder="Age..." /><br />
                    <button type="submit">Submit</button>
                </form>
            </div>
        )
    }

}

export default PostStats
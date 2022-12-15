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
            user_squat: "",
            user_bench: "",
            user_deadlift: "",
            ranks: []
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
    user_squathandler = (event) => {
        this.setState({
            user_squat: event.target.value
        })
    }
    user_benchhandler = (event) => {
        this.setState({
            user_bench: event.target.value
        })
    }
    user_deadlifthandler = (event) => {
        this.setState({
            user_deadlift: event.target.value
        })
    }

    componentDidMount() {
        axios
        
            .get("http://localhost:8000/stats/")
            .then(res => {
                this.setState({ ranks: res.data });
            })
            .catch(err => {
                console.error(err);
            });
    }

    handleSubmit = async (event) => {
        event.preventDefault()

        if (this.state.ranks.length > 0) {
            this.state.ranks.forEach(async rank => {

            await axios.delete(`http://localhost:8000/stats/${rank.id}`)
            await axios.post("http://localhost:8000/stats/", this.state)
                .then(response => {
                    console.log(response)
                    window.location.reload()
                })
                .catch(error =>{
                    console.log(error.response)
                })
            });
        }

        else {
        axios

            .post("http://localhost:8000/stats/", this.state)
            .then(response => {
                console.log(response)
                window.location.reload()
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
                    <label>Squat :</label> <input type="text" value={this.state.user_squat} onChange={this.user_squathandler} placeholder="Squat..." /><br />
                    <label>Bench :</label> <input type="text" value={this.state.user_bench} onChange={this.user_benchhandler} placeholder="Bench..." /><br />
                    <label>Deadlift :</label> <input type="text" value={this.state.user_deadlift} onChange={this.user_deadlifthandler} placeholder="Deadlift..." /><br />
                    <button onClick={this.handleSubmit}>Submit</button>
                </form>
            </div>
        )
    }

}

export default PostStats
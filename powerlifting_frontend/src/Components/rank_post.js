import React, { Component } from 'react'
import axios from 'axios'

class PostRank extends Component {
    constructor(props) {
        super(props)

        this.state = {
            rank: [],
            errorMsg: ""
        }
    }

    // componenetDidMount(){
    //     axios.get("http://localhost:8000/api/tasks")
    //         .then(response => {
    //             console.log(response)
    //             this.setState({
    //                 rank: response.data
    //             })
    //         })
    //         .catch(error => {
    //             console.log(error)
    //             this.setState({
    //                 errorMsg: "Error retrieving data"
    //             })
    //         })
    // }

    componenetDidMount(){
        const axios = require("axios");
        
        axios({
            method: "POST",
            url: "http://localhost:8000/api/tasks",
            
        })
            .then(response => {
                console.log(response)
                this.setState({
                    rank: response.data
                })
            })
            .catch(error => {
                console.log(error)
                this.setState({
                    errorMsg: "Error retrieving data"
                })
            })
    }

    render() {
        const table = {
            margin: '0 auto',
            padding: '0px 0px 5px 0px',
            width: '80%'
        }

        const td ={
            padding: '0px 0px 20px 0px'
        }

        const align ={
            textAlign: 'justify'
        }

        const {rank, errorMsg} = this.state
        return (
            <div>
                Your Rank
                <br></br><br></br>
                <table style={table}>
                    <thead>
                        <tr>
                            <th style={align}>Name</th>
                            <th>Squat Rank</th>
                            <th>Bench Rank</th>
                            <th>Deadlift Rank</th>
                        </tr>
                    </thead>
                    <tbody>
                    {
                        rank.length ?
                        rank.map( rank =>
                            <tr key={rank.id}>
                                <td style={td}>{rank.weight} </td>
                                <td style={td}>{rank.age} </td>
                                <td style={td}>{rank.gender} </td>
                            </tr>
                        ):
                        null
                    }
                    { errorMsg ? <div>{errorMsg}</div> : null}
                    </tbody>
                </table>
            </div>
        )
    }
}

export default PostRank
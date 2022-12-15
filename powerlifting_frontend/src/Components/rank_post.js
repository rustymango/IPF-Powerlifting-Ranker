import axios from 'axios';
import React, { Component, useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';

function PostRank () {

    var postFromResponse = null;
    const [ranks, setRank] = useState({});
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);

    function fetchRank () {

    setLoading(true);
    axios
    
        .get("http://localhost:8000/stats/")
        .then(response => response.data)
        .then((data) => {
            setRank(data)
            console.log(ranks)

        })
        .catch((error) => {
            setError(error.message);
        })
        .finally(() => {
            setLoading(false);
        })
    }

    useEffect(() => {
        fetchRank();
    }, [])


    // function handleClick(event) {
    //     setRank(event.target.value);
    // };

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

    if (ranks?.length > 0) {
        return(
            <div>
                <h1>Your Ranks</h1>
                <table style = {table}>
                    <thead>
                        <tr>
                            {/* <th style = {align}>Name</th> */}
                            <th>Squat Rank</th>
                            <th>Bench Rank</th>
                            <th>Deadlift Rank</th>
                        </tr>
                    </thead>
                    <tbody>
                    {
                        ranks.map(rank =>
                            // <div>
                            <tr key = {rank.id}>
                                <td style={td}>You beat {rank.squat_rank} of squatters in your class</td>
                                <td style={td}>You beat {rank.bench_rank} of benchers in your class</td>
                                <td style={td}>You beat {rank.deadlift_rank} of deadlifters in your class</td>  
                            </tr>
                            ,{/* <button key = {rank.id}
                                onClick = {() => deleteRank(rank.id)}
                                > Get Rank!
                            </button>
                            </div> */}
                        )
                    }
                    </tbody>
                </table>
                {/* <button
                    onClick = {() => DeleteRank()}
                    > Get Rank!
                </button> */}
            </div>
        )
    }
    else {
        return(
            <div>
                <h3>No ranks posted yet</h3>
                {/* <button
                onClick = {() => fetchRank()}
                > Get Rank!
                </button> */}
                {/* {ranks.map(rank =>
                    <div>
                        <button key = {rank.id}
                            onClick = {() => deleteRank(rank.id)}
                            > Get Rank!
                        </button>
                    </div>
                )
                } */}
            </div>
        )
    }

};

export default PostRank
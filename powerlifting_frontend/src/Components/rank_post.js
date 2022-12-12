import axios from 'axios';
import React, { Component, useState, useEffect }  from 'react';
import { useParams } from 'react-router-dom';

function PostRank () {

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
        });
    }

    useEffect(() => {
        fetchRank();
    }, [])

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
                            <tr key = {rank.id}>
                                <td style={td}>You're in the top {rank.squat_rank}</td>
                                <td style={td}>You're in the top {rank.bench_rank}</td>
                                <td style={td}>You're in the top {rank.deadlift_rank}</td>  
                            </tr>
                        )
                    }
                    </tbody>
                </table>
            </div>
        )
    }
    else {
        return(
            <h3>No ranks posted yet</h3>
        )
    }                

};

export default PostRank
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
            ranks.map((rank, index) => {
                console.log(rank);
                return(
                    <div>
                        <p>{rank.bench_rank}</p>
                        <p>{rank.deadlift_rank}</p>
                        <p>{rank.squat_rank}</p>
                    </div>
                )
            })
        )
    }
    else {
        return (<h3>No ranks posted yet</h3>)
    }

};

export default PostRank
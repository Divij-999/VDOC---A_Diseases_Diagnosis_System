import React, { useEffect, useState } from 'react';
import './Articles.css';
import Footer from '../Footer/footer';


function Articles() {
  const [articles, setArticles] = useState([]);
  const apiKey = process.env.REACT_APP_ARTICLE_API_KEY;
  
  const section = 'health'; // You can change this to 'world', 'science', 'technology', etc.

  useEffect(() => {
    // Fetch top articles from NYT API
    fetch(`https://api.nytimes.com/svc/news/v3/content/all/${section}.json?api-key=${apiKey}`)
      .then(response => response.json())
      .then(data => setArticles(data.results))
      .catch(error => console.error('Error fetching articles:', error));
  },[]);

  return (
    <div className="container-fluid" id='article_body' style={{margin:0,padding:0}}>
        <main>
            <h1 align='center' style={{paddingBottom:'36px',lineHeight:'1rem',fontWeight:'bold',lineHeight:'3rem',color:'#2C3E50'}}>New York Times Top Articles</h1>
            <div id="articles-container" className='row'>
                {articles.map((article, index) => (
                <div id="article" key={index} className='col-4'>
                    <div className="card" style={{margin:'30px',height:'500px'}}>
                        <img src={article.multimedia[2].url} id='articleImage' className="card-img-top" alt="."/>
                        <div className="card-body">
                            <h5 className="card-title">{article.title}</h5>
                            <p className="card-text">{article.abstract}</p>
                            <a href={article.url} target="_blank" rel="noopener noreferrer" className="btn" style={{backgroundColor:'#2C3E50',color:'white',position:'absolute',bottom:'20px'}}>Go somewhere</a>
                        </div>
                    </div>
                </div>
                ))}
            </div>
        </main>
        <Footer/>
    </div>
  );
}

export default Articles;

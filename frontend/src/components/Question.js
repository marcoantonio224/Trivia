import React, { Component } from 'react';
import '../stylesheets/Question.css';
import $ from 'jquery';

class Question extends Component {
  constructor(){
    super();
    this.state = {
      visibleAnswer: false,
      questionId:'',
      rating:0
    }
  }

  componentDidMount(){
    this.setState({
      questionId: this.props.id,
      rating: this.props.rating
    });
  }

  flipVisibility() {
    this.setState({visibleAnswer: !this.state.visibleAnswer});
  }

  highlightStar(e, star_number){
    const children = e.target.parentNode.children;
    for(let i = 0; i < star_number; i++) {
      children[i].className = 'star-highlighted';
    }
  }

  removeHighlightStar(e) {
    e.target.className = 'star';
  }

  removeHighlightStars(e){
    // Get the rating element and its children
    const {rating} = this.refs;
    const stars = rating.children;
    for (let star of stars) {
      star.className = 'star';
    }
  }

  updateQuestionRating() {
    const { questionId, rating } = this.state;
    $.ajax({
      url: `/questions/${questionId}`,
      type: "PATCH",
      dataType: 'json',
      contentType: 'application/json',
      data: JSON.stringify({rating:rating}),
      xhrFields: {
        withCredentials: true
      },
      crossDomain: true,
      success: (result) => {
        this.setState({
          rating:0,
          questionId:''
        })
      }
    });
  }

  rateStar(e, star_number) {
    const questionId = e.target.parentNode.id;
    this.setState({
      questionId: Number(questionId),
      rating: star_number
    });

    // Call the api endpoint to update question's rating
    setTimeout(()=>this.updateQuestionRating(), 100)
  }


  render() {
    const { id, question, answer, category, difficulty } = this.props;
    console.log(this.state)
    return (
      <div className="Question-holder">
        <div className="Question">{question}</div>
        <div className="Question-status">
          <img className="category" src={`${category}.svg`}/>
          <div className="difficulty">Difficulty: {difficulty}</div>
          <img src="delete.png" className="delete" onClick={() => this.props.questionAction('DELETE')}/>

        </div>
        <div>
          Rating:
          <div id={id} className="rating" ref={'rating'} onMouseLeave={(e)=>this.removeHighlightStars(e)}>
              <span
                className="star"
                onMouseEnter={(e)=> this.highlightStar(e, 1)}
                onMouseLeave={(e)=> this.removeHighlightStar(e)}
                onClick={(e) => this.rateStar(e, 1)}>&#9734;</span>
              <span
                className="star"
                onMouseEnter={(e)=> this.highlightStar(e, 2)}
                onMouseLeave={(e)=> this.removeHighlightStar(e)}
                onClick={(e) => this.rateStar(e, 2)}>&#9734;</span>
              <span
                className="star"
                onMouseEnter={(e)=> this.highlightStar(e, 3)}
                onMouseLeave={(e)=> this.removeHighlightStar(e)}
                onClick={(e) => this.rateStar(e, 3)}>&#9734;</span>
              <span
                className="star"
                onMouseEnter={(e)=> this.highlightStar(e, 4)}
                onMouseLeave={(e)=> this.removeHighlightStar(e)}
                onClick={(e) => this.rateStar(e, 4)}>&#9734;</span>
              <span
                className="star"
                onMouseEnter={(e)=> this.highlightStar(e, 5)}
                onMouseLeave={(e)=> this.removeHighlightStar(e)}
                onClick={(e) => this.rateStar(e, 5)}>&#9734;</span>
          </div>
        </div>
        <div className="show-answer button"
            onClick={() => this.flipVisibility()}>
            {this.state.visibleAnswer ? 'Hide' : 'Show'} Answer
          </div>
        <div className="answer-holder">
          <span style={{"visibility": this.state.visibleAnswer ? 'visible' : 'hidden'}}>Answer: {answer}</span>
        </div>
      </div>
    );
  }
}

export default Question;

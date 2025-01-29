const upvoteButton = document.getElementById('upvote');
const downvoteButton = document.getElementById('downvote');

upvoteButton.addEventListener('click', function() {
    console.log('up');
    
    this.classList.toggle('active');
    downvoteButton.classList.remove('active');
});

downvoteButton.addEventListener('click', function() {
    console.log('down');
    
    this.classList.toggle('active');
    upvoteButton.classList.remove('active');
});
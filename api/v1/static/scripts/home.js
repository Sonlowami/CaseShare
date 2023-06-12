$(() => {
    //Save the token passed in the URL
    const tokenFromUrl = window.location.search.match(/x-token=[a-zA-Z0-9\._]+/);
    const token = tokenFromUrl[0].split(/=/)[1];
    localStorage.setItem('x-token', token);
  
    //load all posts
    retrievePosts();
  
    //Display a field for the user to write a post and publish it.
    const postField = $('#postField');
      postField.click(() => {
        // Display a field for the user to actually post anything
        const postForm = $('#formPost')
        const headline = $('<input/>').attr('id', 'headline').attr('type', 'text');
        headline.addClass('form-control').attr('placeholder', 'Catch attention with a headline').attr('autofocus');
        const postBody = $('<textarea></textarea>');
        postBody.addClass('form-control mb-3').attr('placeholder', 'Ask others, or share your experience...');
        const button = $('<button></button').addClass('btn btn-sm btn-success mb-2').text('Post').attr('id', 'postButton');
        postField.hide();
        postForm.after(postBody);
        postBody.after(button);
        postForm.prepend(headline);
        // Allow a user to post when they click a button
        button.click(() => {
          const title = headline.val();
          const content = postBody.val();
          $.ajax({
              url: 'http://0.0.0.0:5001/our-apis/v1/posts',
              type: 'POST',
              contentType: 'application/json',
              dataType: 'json',
              headers: {
                  'Accepts': 'application/json',
                  'x-token': localStorage.getItem('x-token')
              },
              data: JSON.stringify({
                  title: title,
                  content: content
              }),
              success: (data, statusPhrase, resp) => {
                if (resp.status === 201) {
                  headline.hide();
                  postBody.hide();
                  postField.show();
                  button.hide()
                  retrievePosts();
                }
              },
              error: (xhr, textStatus, errorMessage) => {
                  if (xhr.status === 403) {
                    window.location.assign('http://0.0.0.0:5000/login');
                  }
                  else {
                    console.log(textStatus);
                    console.log(errorMessage);
                  }
              }
          })
        })
      })
  });
  function retrievePosts() {
    $.ajax({
      url: 'http://0.0.0.0:5001/our-apis/v1/posts',
      type: 'GET',
      dataType: 'json',
      contentType: 'application/json',
      headers: {
        'x-token': localStorage.getItem('x-token')
      },
      success: (data, statusText,resp) => {
        const postsList = $('<ul></ul>')
        data.forEach(element => {
          const postContainer = $('<li></li>').addClass('container d-flex flex-column mb-2 bg-light').css('border', '0.5px solid grey');
          postContainer.attr('id', 'postContainer').attr('data-id', element.id).css('border-radius', '2%');
          const post = $('<div></div>').addClass('d-flex flex-column');
          const postTitle = $('<h3></h3>').text(element.title);
          const postBody = $('<article></article>');
          const paragraphs = element.content.split('\n\n');
          postBody.append(groupParagraphs(paragraphs))
          const actions = $('<div></div>').addClass('row row-cols-2').css('border-top', '1px solid grey');
          const likeButton = $('<button></button>').text('like').addClass('btn btn-link');
          const commentButton = $('<button></button>').text('comment').addClass('btn btn-link').css('border-left', '1px solid black');
          commentButton.click((e) => {
            e.stopPropagation();
            displayCommentField(element.id);
            console.log('Button clicked');
          })
          actions.append(likeButton, commentButton);
          post.append(postTitle, postBody);
          postContainer.append(post, actions);
          postsList.append(postContainer);
          postContainer.click(() => {
            console.log('this is also fired')
            const comments = retrieveComments(element.id);
            postContainer.append(comments);
          });
        });
        $('#mainContentArea').empty().append(postsList);
      },
      error: (xhr) => {
        if (xhr.status === 403) {
          console.log('error caught');
          window.location.assign('http://0.0.0.0:5000/login');
        }
      }
    })
  }
  function retrieveComments(postId) {
    $.ajax({
      url: `http://0.0.0.0:5001/our-apis/v1/posts/${postId}/comments`,
      type: 'GET',
      dataType: 'json',
      contentType: 'application/json',
      headers: {
        'x-token': localStorage.getItem('x-token')
      },
      success: (data, statusText, resp) => {
        if (resp.status === 200) {
          console.log(data);
          const listOfComments = $('<ul></ul>');
          data.forEach(comment => {
            const owner = $('<span></span>').text(`${comment.user.first_name} ${comment.user.last_name}`);
            const timestamps = $('<span></span>').text(comment.updated_at);
            const paragraphs = comment.content.split('\n\n');
            const content = groupParagraphs(paragraphs);
            const commentMetadata = $('<div></div>').addClass('d-flex').append(timestamps, owner);
            const commentContainer = $('<li></li>').addClass('container').append(commentMetadata, content);
            commentContainer.attr('data-id', comment.id);
            listOfComments.append(commentContainer);
            return listOfComments;
          });
        }
      },
      error: (xhr) => {
        if (xhr.status === 404) {
          const noComment = $('<p></p>').text('Be the first one to comment here').addClass('lead');
          return noComment;
        }
      }
    })
  }
  function displayCommentField(post_id) {
    const commentForm = $('<form></form>').addClass('form').attr('id', 'commentForm');
    const commentField = $('<input/>').addClass('form-control').attr('type', 'text');
    const submitButton = $('<input/>').attr('type', 'button').val('Save comment');
    commentForm.append(commentField, submitButton);
    submitButton.click((e) => {
      e.stopPropagation();
      saveComment(post_id, commentField.val());
    });
    $(`[data-id=${post_id}]`).append(commentForm);
  }
  
  function saveComment(post_id, comment) {
    $.ajax({
      url: `http://0.0.0.0:5001/our-apis/v1/posts/${post_id}/comments`,
      type: 'POST',
      dataType: 'json',
      contentType: 'application/json',
      headers: {
        'x-token': localStorage.getItem('x-token')
      },
      data: JSON.stringify({
        content: comment
      }),
      success: (data, statusText, resp) => {
        if (resp.status === 200) {
          console.log('good results');
          retrieveComments(post_id);
        }
      }
    })
  }
  function groupParagraphs(list) {
    const article = $('<article></article>');
    list.forEach(paragraph => {
      article.append($('<p></p>').text(paragraph));
    });
    return article;
  }
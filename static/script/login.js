$(() => {
    const email = $('#email');
    const password = $('#password');
    $('.formLogin').submit((e) => {
      //user wants to be logged in
      e.preventDefault();

      $.ajax({
        url: 'http://0.0.0.0:5001/our-apis/v1/login',
        type: 'POST',
        contentType: 'application/json',
        headers: {
          Accepts: "application/json"
        },
        data: JSON.stringify({
          email: email.val(),
          password: password.val()
        }),
        success: (data, statusPhrase, resp) => {
          console.log(data)
          if (resp.status == 200) {
            //user is successfully logged In. We now store their JWT Token
            const token = data.token;
            const url = data.redirectUrl;
            localStorage.setItem('x-token', token);
            //Send a request to the redirect url
            window.location.assign(`${url}?x-token=${token}`)
          }
        }
      });
    });
});
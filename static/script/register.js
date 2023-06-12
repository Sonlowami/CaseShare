$(() => {
    const title = $('#title');
    const email = $('#email');
    const password = $('#password');
    const comfirmPassword = $('#comfirmPassword');
    const phone = $('#phone');
    const age = $('#age');
    const country = $('#country');
    const first_name = $('#first_name');
    const last_name = $('#last_name');

    comfirmPassword.change((e) => {
      if ($(e.target).val() !== password.val()) {
        const label = $('<p></p>').text('Password does not match!').addClass('text-sm text-danger').attr('id', 'notMatch');
        comfirmPassword.after(label);
      }
      else {
        const label = $('<p></p>').text('Nice. Password match!').addClass('text-sm text-success').attr('id', 'match');
        if ($('#notMatch')) {$('#notMatch').hide();}
        comfirmPassword.after(label);
      }
    });

    $('#registerForm').submit((e) => {
      console.log('register clicked');
      e.preventDefault();
      $.ajax({
        url: 'http://0.0.0.0:5001/our-apis/v1/register',
        type: 'POST',
        contentType: 'application/json',
        dataType: 'json',
        data: JSON.stringify({
          email: email.val(),
          password: password.val(),
          first_name: first_name.val(),
          last_name: last_name.val(),
          country: country.val(),
          age: age.val(),
          title: title.val(),
          phone: phone.val()
        }),
        success: (data, statusText, resp) => {
          console.log(statusText);
          if (resp.status === 201) {
            //tell the user that the account is successfully created and redirect them to the log in page
            const mainContainer = $('#main-container').empty();
            mainContainer.append($('<span></span>').text('Account created successfully!'));
            mainContainer.append($('<a></a>').attr('href', 'http://0.0.0.0:5000/login').text('  Log In Here!'));
          }
        },
        error: (xhr, statusText, errorMessage) => {
          $('#main-container').empty().text(errorMessage);
        }
      })
    })
});
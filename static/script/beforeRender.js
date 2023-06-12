/* This script runs in all jinja templates that inherit from layout.
It defines functions that will check if a user has a token stored in their localStorage,
and if so, redirect the user to their dashboard/homepage.
*/

function checkToken() {
    if (localStorage.getItem('x-token') !== null) {
        return true;
    }
    return false;
}

function redirectHome (url) {
    const logIn = 'http://0.0.0.0:5000/login';
    const register = 'http://0.0.0.0:5000/register';
    const homeLocation = `http://0.0.0.0:5001/home?x-token=${localStorage.getItem('x-token')}`;
    $.ajax({
        url: url,
        type: 'GET',
        headers: {
            'x-token': localStorage.getItem('x-token')
        },
        success: (data) => {
            window.location.assign(homeLocation);
        },
        error: (xhr, statusText, error) => {
            if (xhr.status == 403) {
                window.location.assign(logIn);
            }
            else if (xhr.status == 404) {
                window.location.assign(register);
            }
            else {
                console.log(error);
            }
        }
    })
}
if (checkToken()) {
    const loginStatusUrl = 'http://0.0.0.0:5001/status';
    redirectHome(loginStatusUrl);
}
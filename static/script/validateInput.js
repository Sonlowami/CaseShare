
function check_email() {
    var pattern = /^([\w-\.]+@([\w-]+\.)+[\w-]{2,4})?$/;
    var email = $("#email").val();
    if (pattern.test(email) && email !== "") {
        $("#email_error_message").hide();
        $("#email").css("border-bottom","2px solid #34F458");
    } else {
        $("#email_error_massage").html("Invalid Email");
        $("#email_error_massage").show();
        $("#email").css("border-bottom","2px solid #F90A0A");
        error_email = true;
    }
}

function check_password() {
    var password_length = $("#password").val().length;
    if (password_length < 8) {
        $("#password_error_message").html("Atleast 8 Characters");
        $("#password_error_message").show();
        $("#password").css("border-bottom","2px solid #F90A0A");
        error_password = true;
    } else {
        $("#password_error_message").hide();
        $("#password").css("border-bottom","2px solid #34F458");
    }  
}  

var error_email = false;
var error_password = false;

$(function() {

$("#email_error_message").hide();
$("#password_error_message").hide();

$("#email").focusout(function() {
    check_email();
});
$("#password").focusout(function() {
    check_password();
});

$("#main-container").submit(function() {
error_email = false;
error_password = false;

check_email();
check_password();
});
});
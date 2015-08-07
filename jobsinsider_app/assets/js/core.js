/**
 * Created by azhar on 8/7/15.
 */

// for login account for the user

function login_account()
{
    $.ajax(
        {
            url : "/accounts/login/", // the endpoint
            type : "POST", // http method
            data: $('#login_user').serialize(),
            success: function(json)
            {
                console.log(json);
            },
            error: function(json)
            {
                console.log(json);
            }

        }
    );

}



//for forgot password user

function forgot_password()
{
    $.ajax(
        {
            url : "/accounts/forgot/", // the endpoint
            type : "POST", // http method
            data: $('#forgot_form').serialize(),
            success: function(json)
            {
                console.log(json);
            },
            error: function(json)
            {
                console.log(json);
            }

        }
    );
}

//for create account
//register_form

function register_account()
{
    $.ajax(
        {
            url : "/accounts/register/", // the endpoint
            type : "POST", // http method
            data: $('#register_form').serialize(),
            success: function(json)
            {
                console.log(json);
            },
            error: function(json)
            {
                console.log(json);
            }

        }
    );
}
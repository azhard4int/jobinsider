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
            success: function(response)
            {
                response = JSON.parse(response);
                if (response.status==1){
                    window.location.href = '/private/members/';
                }
                else if(response.status==2){
                window.location.href = '/user/create-basic-profile/?step=0/';
                }
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

// Currently not using this funciton..

function forgot_set()
{
    $.ajax(
        {
            url : "/accounts/forgot/newpassword", // the endpoint
            type : "POST", // http method
            data: $('#forgot_set').serialize(),
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
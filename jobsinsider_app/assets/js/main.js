$(document).ready(function()
{
        $('#forgot_form').on('submit', function()
        {
            event.preventDefault();
            forgot_password();
            return false;
        });
});

function forgot_password()
{
    $.ajax(
        {
            url : "/accounts/forgot/", // the endpoint
            type : "POST", // http method
            data: $('#forgot_form').serialize(),
            success: function(json)
            {
                console.log(GetObjectKeyIndex(json, 'status'));
            },
            error: function(json)
            {
                console.log(GetObjectKeyIndex(json, 'status'));
            }

        }
    );
}
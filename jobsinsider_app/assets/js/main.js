$(document).ready(function()
{

        $('#login_user').on('submit', function()
        {
            event.preventDefault();
            login_account();
            return false;
        });

        $('#forgot_form').on('submit', function()
        {
            event.preventDefault();
            forgot_password();
            return false;
        });

         $('#register_form').on('submit', function()
        {
            event.preventDefault();
            register_account();
            return false;
        });

});

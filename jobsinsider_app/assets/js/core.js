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
                else if(response.status==3){
                    window.location.href = '/accounts/confirm-email/';
                }
            },
            error: function(json)
            {
                console.log(json);
                console.log('dsadas');
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


//admin pannel side.

$('#add_category_admin').on('submit', function(event)
{
   event.preventDefault();
    $.ajax({
        url: '/private/members/categories/add_category',
        type: 'POST',
        data: $('form#add_category_admin').serialize(),
        success: function(response)
        {
            console.log('here now');

        },
        error: function(response)
        {

        }
    })
    return false;
});

$('.disable_cat_btn').on('click', function(event)
{

    valuedata = ($(this).attr('value'));
    $.ajax({
        url: '/private/members/categories/disable/?cat_id=' + valuedata,
        type: 'POST',
        data: {
            'category_id': valuedata,
            csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value
        },
        success:function(response)
        {
            response = JSON.parse(response);
            if (response.status=='True')
            {
                $('.display_message').html('Campaign Status Enabled');

            }
        },
        error: function(response)
        {

        }


    });
});

$('.enable_cat_btn').on('click', function(event)
{
    valuedata = ($(this).attr('value'));
    $.ajax({
        url: '/private/members/categories/enable/?cat_id=' + valuedata,
        type: 'POST',
        data: {
            'category_id': valuedata,
            csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value
        },
        success:function(response)
        {
            response = JSON.parse(response);
            if (response.status=='True')
            {
                $('.display_message').html('Campaign Status Enabled');

            }
        },
        error: function(response)
        {

        }


    });

});

$('.delete_cat_btn').on('click', function(event)
{
    valuedata = ($(this).attr('value'));
    $.ajax({
        url: '/private/members/categories/delete/?cat_id=' + valuedata,
        type: 'POST',
        data: {
            'category_id': valuedata,
            csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value
        },
        success:function(response)
        {
            response = JSON.parse(response);
            if (response.status=='True')
            {
                $('.display_message').html('Category Deleted Successfully!');

            }
        },
        error: function(response)
        {

        }


    });

});

$('.details_cat_btn').on('click', function(event)
{
    valuedata = ($(this).attr('value'));
    $.ajax({
        url: '/private/members/categories/details/?cat_id=' + valuedata,
        type: 'POST',
        data: {
            'category_id': valuedata,
            csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value
        },
        success:function(response)
        {
            response = JSON.parse(response);
            if (response.status=='True')
            {
                $('.display_message').html('Category Deleted Successfully!');

            }
        },
        error: function(response)
        {

        }


    });

});

$('#edit_category_form').on('submit', function(event)
{
    alert('up here');
    //valuedata = ($(this).attr('value'));
    $.ajax({
        url: '/private/members/categories/editcategory/',
        type: 'POST',
        data: $('#edit_category_form').serialize(),
        success:function(response)
        {
            response = JSON.parse(response);
            if (response.status=='True')
            {
                $('.display_message').html('Category Deleted Successfully!');

            }
        },
        error: function(response)
        {
            console.log(response);
        }


    });




});


// Skill view funcitons.

$('a.enable_skill_btn').on('click', function(event)
{
    valuedata = ($(this).attr('value'));
    alert(valuedata);
    $.ajax({
        url: '/private/members/categories/skill_enable/',
        type: 'POST',
        data: {
            'skill_id':valuedata,
            'csrfmiddlewaretoken': document.getElementsByName('csrfmiddlewaretoken')[0].value},
        success:function(response)
        {
            response = JSON.parse(response);
            if (response.status=='True')
            {
                $('.display_message').html('Category Deleted Successfully!');

            }
        },
        error: function(response)
        {
            console.log(response);
        }


    });

});

$('a.disable_skill_btn').on('click', function(event)
{
    valuedata = ($(this).attr('value'));
    alert(valuedata);
    $.ajax({
        url: '/private/members/categories/skill_disable/',
        type: 'POST',
        data: {
            'skill_id':valuedata,
            'csrfmiddlewaretoken': document.getElementsByName('csrfmiddlewaretoken')[0].value},
        success:function(response)
        {
            response = JSON.parse(response);
            if (response.status=='True')
            {
                $('.display_message').html('Category Deleted Successfully!');

            }
        },
        error: function(response)
        {
            console.log(response);
        }


    });

});

$('a.delete_skill_btn').on('click', function(event)
{
    alert('up here');
    valuedata = ($(this).attr('value'));
    $.ajax({
        url: '/private/members/categories/skill_delete/',
        type: 'POST',
        data: {
            'skill_id':valuedata,
            'csrfmiddlewaretoken': document.getElementsByName('csrfmiddlewaretoken')[0].value},
        success:function(response)
        {
            response = JSON.parse(response);
            if (response.status=='True')
            {
                $('.display_message').html('Category Deleted Successfully!');

            }
        },
        error: function(response)
        {
            console.log(response);
        }


    });

});


$('#edit_skill_btn').on('submit', function(event)
{
    alert('up here');
    valuedata = ($(this).attr('value'));
    $.ajax({
        url: '/private/members/categories/skill_delete/',
        type: 'POST',
        data: $('#edit_skill_btn').serialize(),
        success:function(response)
        {
            response = JSON.parse(response);
            if (response.status=='True')
            {
                $('.display_message').html('Skill Edited Successfully!');

            }
        },
        error: function(response)
        {
            console.log(response);
        }


    });

});



/**
 * Created by azhar on 8/7/15.
 */

// for login account for the user

function getcsrf()
{
    csrfmiddlewaretoken = document.getElementsByName('csrfmiddlewaretoken')[0].value
    return csrfmiddlewaretoken
}

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
                    window.location.href = '/user/create-basic-profile/?step=0';
                }
                else if(response.status==3){
                    window.location.href = '/accounts/confirm-email/';
                }
                else if(response.status==-1){

                    $('label.l0_form .error_message').html('There is no username exist with your entered username.');
                    $('label.l0_form .error_message').show();
                    //console.log(response.status);
                    //$('.error_message').html(response.status);
                }
            },
            error: function(response)
            {
                //console.log(response);
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
            success: function(response)
            {
                json = JSON.parse(response);
                console.log(json);
                if(json.status=='-1')
                {
                     $('label.l0_form .error_message').html('There is no email exist which you have entered');
                    $('label.l0_form .error_message').show();
                }
                else if (json.status==1)
                {

                    $('label.l0_form .error_message').hide();
                    $('label.l0_form .success').html('Please check your email address to reset password and follow the instructions on it');
                    $('label.l0_form .success').show();
                }
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
    console.log('here now');
    formdata = new FormData('#set_password');
    console.log(formdata);
    var email_details  = document.getElementsByName('email')[0].value;
    var password =  document.getElementsByName('password')[0].value;
    var csrfmdi = document.getElementsByName('csrfmiddlewaretoken')[0].value;
    console.log(email_details);
    $.ajax(
        {
            url : "/accounts/forgot/newpassword/", // the endpoint
            type : 'POST', // http method
            data: {'email':email_details,
                'password': password,
                'csrfmiddlewaretoken': csrfmdi
            },
            success: function(json)
            {
                json_data = JSON.parse(json);
                if(json_data.status==1)
                {
                     $('label.l0_form .error_message').hide();
                    $('label.l0_form .success').html('New Password has been set');
                    $('label.l0_form .success').show();
                }

            },
            error: function(json)
            {
                console.log(json);
            }

        }
    );
    return false;
}


// resend the confrimation email to the user


$('.c0_email_btn').on('click', function(event)
{
    event.preventDefault();
    csrf = getcsrf();
    $.ajax(
        {
            type: "POST",
            url: '/accounts/resend-confirmation/',
            data: {csrfmiddlewaretoken: csrf},
            success:function(data)
            {
                resp = JSON.parse(data);
                if(resp.status==1)
                {
                    $('.status_msg').html('A resend confirmation email has been sent to your email address');
                    $('.status_msg').show();
                }
            }
        }
    );


    return false;
});


//admin pannel side.

$('#add_category_admin').on('submit', function(event)
{
    event.preventDefault();
    var data = new FormData($('#add_category_admin').get(0));
    $.ajax({
        url: '/private/members/categories/add_category',
        type: 'POST',
        data: data,
        cache: false,
        processData: false,
        contentType: false,
        success: function(response)
        {
            resp = JSON.parse(response);
            if(resp.status==1)
            {
                window.location.href =  '/private/members/categories/'
            }

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


$('#edit_skill_form').on('submit', function(event)
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


    //User dashboard javascript

    $('a.c0_cat_main').on('click', function()
    {
        $(this).addClass('activated');
        //event.preventDefault();
        valuedata = ($(this).attr('value'));
        $.ajax({
            'url': '/user/skills_list/',
            'type': 'POST',
            'data': {
                'cat_id': valuedata,
                'csrfmiddlewaretoken': document.getElementsByName('csrfmiddlewaretoken')[0].value},
            success:function(response){
                    var data_response = (JSON.parse(response));
                    console.log(data_response);
                    var data_insert = "";
                    var skill_cat_id = '';
                    for (var i=0; i<data_response.length; i++){
                        console.log(data_response[i].fields['skill_name']);
                        console.log(data_response[i].pk);
                        skill_cat_id = data_response[i].fields['category'];
                        data_insert += "<div class='skill_btn'><label><input class='skillvalues' type='checkbox' value='"+data_response[i].pk+"' name='skillcheck'><span>" + data_response[i].fields['skill_name'] + "</span></div>";
                    }

                    $('.s0_skill'+ skill_cat_id).html(data_insert);
            },
            error:function(response)
            {
                console.log(response);
            }

        });
        return false;
    });


// Passing the skills value to user skills view

$('#skills_form').on('submit', function(event)
{
    event.preventDefault();
    var inputElements = document.getElementsByClassName('skillvalues');
    var checkboxes = '';
    for (var i=0; i<inputElements.length; i++)
    {
        if(inputElements[i].checked)
        {
            if(i==0)
            {
                checkboxes += inputElements[i].value;
            }
            else{
                checkboxes += ',' + inputElements[i].value;
            }


        }

    }

    var category_id = $('a.c0_cat_main.activated').attr('value');
    console.log(category_id);
    $.ajax({
        'url':'/user/skills/',
        'type':'POST',
        'data':{
            'skills_value': checkboxes,
            'csrfmiddlewaretoken':document.getElementsByName('csrfmiddlewaretoken')[0].value,
            'category_id':category_id,
        },
        success:function(response)
        {
            response = JSON.parse(response);
            console.log(response.status);
            if((response.status=true) || (response.status='True')){
                window.location.href  = '?step=1'
            }

        },
        error:function(response)
        {
            response = JSON.parse(response);
        }
    });


    return false;
});

//cv upload option up here...

$('a.cv_option').on('click', function(event){
    var attrvalue = $(this).attr('value');
    if(attrvalue==0)
    {
        $('a.cv_decision').html('Upload CV');
        $('.cv_decision').attr('value', 'Upload Your CV');
        $('.cv_decision').attr('data-toggle', 'modal');
        $('.cv_decision').attr('data-target', '#myModal');
        $('.decision_wise').attr('value', 1)
    }
    else if(attrvalue==1){
        $('a.cv_decision').html('Contine to CV Builder');
        $('.cv_decision').attr('value', 'Contine to CV Builder');
        $('.decision_wise').attr('value', 2)
    }

});


//Basic profile event triggered!

$('#bio_form').on('submit', function(event)
{
    event.preventDefault();
    var data = new FormData($('#bio_form').get(0));
    console.log(data);
    $.ajax({
        url: '/user/profile_bio/',
        type: 'POST',
        data: data,
        cache: false,
        processData: false,
        contentType: false,
        success:function(response)
        {
            response = JSON.parse(response);
            if(response.status==true)
            {
                window.location.href="?step=2"  // CV selection region
            }
        }
    });
    return false;


});


//cv upload file event triggered!

$('#user_decision').on('submit', function(event)
{
    event.preventDefault();
    var value_check = $('.decision_wise').attr('value');
    //if(value_check==1)
    //{
    //    //cv upload dialog box
    //    console.log('dasdas');
    //}
    //else
    //
    if (value_check==2)
    {
        //move to the cv builder page
    }
    else if(value_check==0){
        alert('please select the value first')
    }

    return false;

});

//cv uploaded file handler.


$('#user_cv').on('submit', function(event)
{
    event.preventDefault();
    var data = new FormData($('#user_cv').get(0));
    console.log(data);
    $.ajax({
        url: '/user/profile_cv/',
        type: 'POST',
        data: data,
        cache: false,
        processData: false,
        contentType: false,
        success:function(response)
        {
            response = JSON.parse(response);
            if(response.status==true)
            {
                window.location.href="?step=2"  // CV selection region
            }
        }
    });
    return false;


});

// add more employemnts history

$('.add_employment').on('click', function(event)
{
    event.preventDefault();
    var getCount = $('.company_count').attr('value');
    $.ajax(
    {
        url: '/user/add_user_employment/',
        type: 'POST',
        data: {'csrfmiddlewaretoken': document.getElementsByName('csrfmiddlewaretoken')[0].value},
        success:function(response)
        {
            getCount++;
            $('.company_count').attr('value', getCount);
            $('.more_form').append(response)
            console.log(response);
        },
        error: function(resposne){

        }

    });
    return false;
});

$('#add_bio_employment').on('submit', function(event)
{
    //var getCount = $('.company_count').attr('value');
    event.preventDefault();
    formdata = new FormData('#add_bio_employment');
    $.ajax(
    {
        url: '/user/add_employment/',
        type: 'POST',
        data: $('#add_bio_employment').serialize(),
        success:function(response)
        {
            resp = JSON.parse(response);
            if (resp.status==true){
                window.location.href="?step=4"
            }
            else if(resp.status==false)
            {
                window.location.href="?step=3"
            }
            //getCount++;
            //$('.company_count').attr('value', getCount);
            //$('#user_employemnt').append(response)
            //console.log(response);
        },
        error: function(resposne){
        }

    });
    return false;
});
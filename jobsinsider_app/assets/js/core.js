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
    wait_it('#login_user');
    $.ajax(
        {

            url : "/accounts/login/", // the endpoint
            type : "POST", // http method
            data: $('#login_user').serialize(),
            success: function(response)
            {
                wait_it_hide('#login_user');
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
                else if(response.status==4){
                    window.location.href = '/company/index';
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
                wait_it_hide('#login_user');
                //console.log(response);
            }

        }
    );

}



//for forgot password user

function forgot_password()
{
    wait_it('body');
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
                    wait_it_hide('body');
                }
                else if (json.status==1)
                {

                    wait_it_hide('body');
                    $('label.l0_form .error_message').hide();
                    $('label.l0_form .success').html('Please check your email address to reset password and follow the instructions on it');
                    $('label.l0_form .success').show();
                }
            },
            error: function(json)
            {
                wait_it_hide('body');
                console.log(json);
            }

        }
    );
}

//for create account
//register_form

function register_account()
{
    wait_it('#register_form');
    $.ajax(
        {
            url : "/accounts/register/", // the endpoint
            type : "POST", // http method
            data: $('#register_form').serialize(),
            success: function(json)
            {
                resp = JSON.parse(json);
                wait_it_hide('#register_form');
                if(resp.status==false)
                {
                    $('label.l0_form .error_message').html(resp.response);
                    $('label.l0_form .error_message').show();
                }
                if(resp.status==true)
                {
                    console.log('registered');
                    message_display('Verification Link has been Emailed to You!', 1);
                    setTimeout(function(){
                       window.location.href = '/accounts/login/';
                    }, 2000);
                }
            },
            error: function(json)
            {
                wait_it_hide('#register_form');
                message_display('Something Went Wrong, Notify Administrators!', 0)
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
    wait_it('body');
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
                    wait_it_hide('body');
                    $('.status_msg').show();
                }
            },
            error:function(m)
            {
                wait_it_hide('body');

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
                window.location.reload();

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

$('.user_bio_form').on('click', function(event)
{
    event.preventDefault();
    if($('#id_user_portrait').val()=='')
    {
        alert('Please upload your profile picture.');
    }
     if($('#id_user_zipcode, #id_user_phone_no').val()=='')
        {
            $('#id_user_zipcode, #id_user_phone_no').focus();
            $('#id_user_zipcode, #id_user_phone_no').css('border-color', 'red');
        }
    else{

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
                    window.location.href="/user/profile_cv"  // CV selection region
                }
            }
         });
     }
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
                window.location.href="/user/add_employment/";  // CV selection region
            }

        }
    });
    return false;


});

// add more employemnts history
var getCountValue = 0;
//$('.add_employment').on('click', function(event)
//{
//    event.preventDefault();
//    var getCount = $('.company_count').attr('value');
//    $.ajax(
//    {
//        url: '/user/add_user_employment/',
//        type: 'POST',
//        data: {'csrfmiddlewaretoken': document.getElementsByName('csrfmiddlewaretoken')[0].value},
//        success:function(response)
//        {
//            getCount++;
//            getCountValue++;
//            console.log(response);
//            $('.company_count').attr('value', getCount);
//            $('.more_form').append("<div class='form_value_"+getCountValue+"'>"+response);
//            $('.more_form'),append('<div class="removeValue" value="'+ getCountValue  + '"');
//            console.log(response);
//        },
//        error: function(resposne){
//
//        }
//
//    });
//    return false;
//});



//through jquery clone

_count = 0;
$('.add_employment').on('click', function(event) {
    if($('input[type=text][name=company_name]').val()=='')
    {
        return false;
    }
    if(($('input[type=text][name=company_location]').val())==0)
    {
        return false;

    }
    if(($('input[type=text][name=company_title]').val())==0)
    {
        return false;
    }
    if(($('input[type=text][name=company_role]').val())==0)
    {
        return false;
    }


    $('.whl').clone().appendTo('.more_form').fadeIn();
    var _value = "<div class='hide_field' value="+ _count + "</div>";
    //$('.more_form').appendTo("<div class='hide_field' value='"+ _count + "'></div>");
    $('.datepicker').datepicker("refresh")

});


//education update for the page.
$('.employment_info').on('click', function(e)
{
    //var getCount = $('.company_count').attr('value');
    e.preventDefault();
    if($("#id_company_name, #id_company_location, #id_company_worktitle, #id_company_role ").val()=='')
    {
        $('#id_company_name, #id_company_location, #id_company_worktitle, #id_company_role ').focus();
        $('#id_company_name, #id_company_location, #id_company_worktitle, #id_company_role').css('border-color', 'red');
    }
    else
    {
        formdata = new FormData('#add_bio_employment');
        $.ajax(
        {
            url: '/user/add_employment/',
            type: 'POST',
            data: $('#add_bio_employment').serialize(),
            success:function(response)
            {
                $('.list_education').show('slow');
                $('.company_bio_appended').append(response);
            },
            error: function(response){
            }

        });
    }
    return false;
});

$(document).on('click', '.user_company_delete', function(e)
{
    e.preventDefault();
    var id = $(this).attr('value');
    $('.user_employment_'+id).remove();
    var csrfmdi = document.getElementsByName('csrfmiddlewaretoken')[0].value;
    $.ajax({
        type:'POST',
        url:'/user/remove_employment/' + id + '/',
        data:{
            'csrfmiddlewaretoken': csrfmdi
        },
        success:function(m)
        {
            resp = JSON.parse(m);
            if(resp.status==true)
            {
                console.log('Removed');
            }
        }
    });
    return false;
});



//user cv builder education


var educount = 0;
$('.add_edu').on('click', function(event)
{
    event.preventDefault();
    if(educount<2)
    {
        $('.education_single').clone().appendTo('.add_more_education').fadeIn();
        educount++;
    }
    else{
        alert('You can add only 3-5 Higher Educations');
    }

    $('.add_more_education').find("#id_degree_from").datepicker();
    $('.add_more_education').find("#id_degree_to").datepicker();
    return false;
});


$('.education_info').on('click', function(event) {

    event.preventDefault();
    if($("#id_user_institute, #id_user_degree").val()=='')
    {
        $('#id_user_institute, #id_user_degree').focus();
        $('#id_user_institute, #id_user_degree').css('border-color', 'red');
    }
    else {
        $.ajax({
            type: 'post',
            url: '/user/education/',
            data: $('#add_edu_form').serialize(),
            success: function (m) {
                $('.user_education_append').append(m);
            },
            error: function () {

            }
        });
    }
    return false;
});



$(document).on('click', '.user_education_delete', function(e)
{
    e.preventDefault();
    var id = $(this).attr('value');
    $('.user_education_'+id).remove();
    var csrfmdi = document.getElementsByName('csrfmiddlewaretoken')[0].value;
    $.ajax({
        type:'POST',
        url:'/user/remove_education/' + id + '/',
        data:{
            'csrfmiddlewaretoken': csrfmdi
        },
        success:function(m)
        {
            resp = JSON.parse(m);
            if(resp.status==true)
            {
                console.log('Removed');
            }
        }
    });
    return false;
});

//cv builder continue

$('.cv_builder_status').on('click', function(e)
{
    var csrfmdi = document.getElementsByName('csrfmiddlewaretoken')[0].value;
    $.ajax(
        {
            type:'POST',
            url:'/user/is_cv_builder/',
            data:{
                'csrfmiddlewaretoken':csrfmdi
            },
            success:function(m)
            {
                resp  = JSON.parse(m);
                if(resp.status=true)
                {
                    window.location.href = '/user/add_employment/';
                }

            },
            error:function(m){

            }


        }
    )
    return false;
});

//complete profile

$('.complete_profile').on('click', function(e)
{
    var csrfmdi = document.getElementsByName('csrfmiddlewaretoken')[0].value;
    $.ajax(
        {
            type:'POST',
            url:'/user/complete_profile/',
            data:{
                'csrfmiddlewaretoken':csrfmdi
            },
            success:function(m)
            {
                resp  = JSON.parse(m);
                if(resp.status=true)
                {
                    window.location.href = '/user/dashboard/';
                }

            },
            error:function(m){

            }


        }
    )
    return false;
});

//user profile update


$('.personal_info').on('submit', function() {
    //var getCount = $('.company_count').attr('value');
    event.preventDefault();
    $.ajax(
        {
            url: '/user/u/',
            type: 'POST',
            data: $('.personal_info').serialize(),
            success:function(m){
                resp = JSON.parse(m)
                if(resp.status==true)
                {
                    window.location.reload();
                }
            }
        }
    );
    return false;

});


//change user password

$('.change_password_user').on('submit', function(e) {
    //var getCount = $('.company_count').attr('value');
    e.preventDefault();
    $.ajax(
        {
            url: '/user/u/changepassword/',
            type: 'POST',
            data: $('.change_password_user').serialize(),
            success:function(m){
                resp = JSON.parse(m)
                if (resp.status==-3)
                {
                    $('.error_main').html('');
                    $('.error_main').html('No such user found in the database')
                }
                else if (resp.status==-2)
                {
                    $('.error_main').html('');
                    $('.error_main').html('Current password does not match.')
                }
                else if(resp.status==-1)
                {
                    $('.error_main').html('');
                    $('.error_main').html('Both new password does not match.')
                }
                else if(resp.status==1)
                {
                    $('.error_main').html('');
                    $('success_main').html('');
                    $('success_main').html('Password Successfully Updated')

                }


            }
        }
    );
    return false;

});

//Company Section JS

$('.company_detail').on('click', function(e){
    e.preventDefault();
    if($('#id_company_name, #id_your_role, #id_company_url, #id_company_industry').val()=='')
        {
            $('#id_company_name, #id_your_role, #id_company_url, #id_company_industry').focus();
            $('#id_company_name, #id_your_role, #id_company_url, #id_company_industry').css('border-color', 'red');
        }
    $.ajax(
        {
            type:'post',
            url:'/company/index/',
            data:$('#company_profile').serialize(),
            success:function(m)
            {
                resp = JSON.parse(m);
                if(resp.status==true)
                {
                    window.location.href = '/company/index/'
                }
                else{
                    $('error_m').html('Some Error Incurred');
                }
            }
        }
    );
    return false;
});


$('.change_company_password').on('click', function(e){
    e.preventDefault();
    $.ajax(
        {
            type:'post',
            url:'/company/changepassword/',
            data:$('.change_company_pass_form').serialize(),
            success:function(m){
                resp = JSON.parse(m)
                if (resp.status==-3)
                {
                    $('.error_main').html('');
                    $('.error_main').html('No such user found in the database')
                }
                else if (resp.status==-2)
                {
                    $('.error_main').html('');
                    $('.error_main').html('Current password does not match.')
                }
                else if(resp.status==-1)
                {
                    $('.error_main').html('');
                    $('.error_main').html('Both new password does not match.')
                }
                else if(resp.status==1)
                {
                    $('.error_main').html('');
                    $('success_main').html('');
                    $('success_main').html('Password Successfully Updated')

                }
            }
        }
    );
    return false;
});



//job advertisement view

$('.job_advertisement').on('click', function(event)
{


    if($('#id_job_title').val()=='')
    {
        //, #id_job_position, #id_salary_from, #id_salary_to
            $('#id_job_title').focus();
            $('#id_job_title').css('border-color', 'red');
            exit;
    }
    else if($('#id_job_position').val()=='')
    {
        $('#id_job_position').focus();
        $('#id_job_position').css('border-color', 'red');

    }
    else if($('#id_salary_from').val()=='')
    {
        $('#id_salary_from').focus();
        $('#id_salary_from').css('border-color', 'red');
    }
    else if($('#id_salary_to').val()=='')
    {
        $('#id_salary_to').focus();
        $('#id_salary_to').css('border-color', 'red');
    }
    else{
        var formElement = document.querySelector('form');
        var form_data = $('#jobadvert_form').serialize();// new FormData(formElement);
        var salary_currency = $('#salary_currency').val();
        var job_description = (tinyMCE.activeEditor.getContent({format : 'raw'}));
        var csrfmdi = document.getElementsByName('csrfmiddlewaretoken')[0].value;
        if($('#evaluation_test_label').attr('value')==0)
        {
            evaluation_id = 0;
        }
        else{
            evaluation_id = $('.evaluation_template').val();
        }
        $.ajax(
            {
                url:'/company/create-job/',
                type:'POST',
                data:{
                    'form_val': form_data,
                    'csrfmiddlewaretoken': csrfmdi,
                    'description': job_description,
                    'salary_currency': salary_currency,
                    'evaluation_id':evaluation_id
                },
                success:function(m)
                {
                    resp = JSON.parse(m);
                    if(resp.status==true)
                    {
                        window.location.href= '/company/settings-job/'+ resp.last_inserted;
                    }
                },
                error:function(m)
                {

                }
            }
        );
    }
    return false;
});

//to show the date for apply by

$('#apply_by_date').change(function(e){
    e.preventDefault();
    if(this.checked)
    {
        $('.apply_datepicker').show();
    }
    else{
        $('.apply_datepicker').hide();
    }
    return false;
});


//job settings page after the job creation
$('.job_ad_settings').on('click', function(e)
{

    e.preventDefault();
    var csrfmdi = document.getElementsByName('csrfmiddlewaretoken')[0].value;
    var is_email = 0;
    var is_apply_by = 0;
    if($('#resume_email').is(":checked"))
    {
        is_email = 1;
    }
    if($('#apply_by_date').is(":checked"))
    {
        is_apply_by = 1;
    }
    date_value = $('.apply_by_datevalue').val();
    //alert(date_value);
    $.ajax(
        {
            url:'/company/settings-job/' + $('.job_id').attr('value'),
            type:'POST',
            data: {
                'csrfmiddlewaretoken': csrfmdi,
                'is_email': is_email,
                'is_apply_by': is_apply_by,
                'date_value': date_value
            },
            success:function(m)
            {
                resp = JSON.parse(m);
                if(resp.status==true)
                {
                    window.location.href = '/company/finalize-job/';
                }
            },
            error:function(m)
            {

            }
        }
    );
    return false;

});

//posted jobs

is_active_dropdown  = 0;
$('.action_posted_job').on('click', function(e)
{
    e.preventDefault();
    get_id = $(this).attr('value');
    if(is_active_dropdown==0)
    {
        $('.menu_id_'+get_id).show();
        is_active_dropdown = 1;
    }
    else{
        $('.menu_id_'+get_id).hide();
        is_active_dropdown=0;
    }

    console.log(get_id);
    return false;
});

$('.delete_job_menu').on('click', function(e)
{
    e.preventDefault();
    get_id = $(this).attr('value');
    csrfmdi = document.getElementsByName('csrfmiddlewaretoken')[0].value;
    $.ajax(
        {
            type:'POST',
            url:'/company/delete-job/' + get_id   + '/',
            data: {
                'csrfmiddlewaretoken': csrfmdi
            },
            success:function(m)
            {
                var resp = JSON.parse(m);
                if(resp.status==true){
                    $('.posted_job_remove_'+get_id).remove();
                    $('html,body').animate({
                            scrollTop: $('.message_details').offset().top},
                        'slow');

                    console.log('here');
                    //$('.message_details').html('Job has been deleted successfully!')
                    message_display('Job has been deleted successfully!', 1);
                }
            }
        }
    );
    return false;
});

$('.pause_job_menu').on('click', function(e)
{
    e.preventDefault();
    get_id = $(this).attr('value');
    csrfmdi = document.getElementsByName('csrfmiddlewaretoken')[0].value;
    $.ajax(
        {
            type:'POST',
            url:'/company/pause-job/' + get_id   + '/',
            data: {
                'csrfmiddlewaretoken': csrfmdi
            },
            success:function(m)
            {
                var resp = JSON.parse(m);
                if(resp.status==true){
                    //$('.message_details').html('Job has been deleted successfully!')
                    message_display('Job has been Paused successfully!', 1);
                    setTimeout(function(){
                       window.location.reload(1);
                    }, 1000);
                }
            }
        }
    )
    return false;
});

//edit job details

$('.job_advertisement_edit').on('click', function(event)
{
    var formElement = document.querySelector('form');
    var form_data = $('#jobadvert_form').serialize();// new FormData(formElement);
    var job_description = (tinyMCE.activeEditor.getContent({format : 'raw'}));
    var csrfmdi = document.getElementsByName('csrfmiddlewaretoken')[0].value;
    var id_value = $('.jobid_value').attr('value');
    //alert(id_value);
    if($('#evaluation_test_label').attr('value')==0)
        {
            evaluation_id = 0;
        }
        else{
            evaluation_id = $('.evaluation_template').val();
        }
    $.ajax(
        {
            url:'/company/job/edit/' + id_value,
            type:'POST',
            data:{
                'form_val': form_data,
                'csrfmiddlewaretoken': csrfmdi,
                'description': job_description,
                evaluation_id:evaluation_id
            },
            success:function(m)
            {
                resp = JSON.parse(m);
                console.log(resp);
                if(resp.status==true)
                {
                    message_display('Job Edited Successfully', 1)
                    //window.location.href= '/company/settings-job/'+ resp.last_inserted;
                }
            },
            error:function(m)
            {

            }
        }
    );

    return false;
});

//applying candidates

$('.apply_job').on('click', function(event)
{
    event.preventDefault();
    var csrfmdi = document.getElementsByName('csrfmiddlewaretoken')[0].value;
    var id_value = $('.job_apply_btn').attr('value');
    $.ajax(
        {
            url:'/jobs/detail/' + id_value + "/",
            type:'POST',
            data:{
                'csrfmiddlewaretoken': csrfmdi
            },
            success:function(data)
            {
                resp = JSON.parse(data);
                console.log(resp);
                if(resp.status==true)
                {
                    message_display(resp.response, 1)
                }
            },
            error:function(data)
            {

            }
        }
    );
    return false;
});

//
function evaluation_apply_job(evaluation_result)
{
    var csrfmdi = document.getElementsByName('csrfmiddlewaretoken')[0].value;
    var id_value = $('.evaluation_apply_job_e').attr('value');
    $.ajax(
        {
            url:'/jobs/detail/' + id_value + "/",
            type:'POST',
            data:{
                'csrfmiddlewaretoken': csrfmdi,
                'evaluation_score':evaluation_result
            },
            success:function(data)
            {
                resp = JSON.parse(data);
                console.log(resp);
                if(resp.status==true)
                {
                    message_display(resp.response, 1)
                }
            },
            error:function(data)
            {

            }
        }
    );
    return false;
};



$('.add_favorite').on('click', function(event)
{
    event.preventDefault();
    var csrfmdi = document.getElementsByName('csrfmiddlewaretoken')[0].value;
    var id_value = $('.add_favorite').attr('value');
    $.ajax(
        {
            url:'/jobs/add_favorite_job/',
            type:'POST',
            data:{
                'csrfmiddlewaretoken': csrfmdi,
                'job_id': id_value
            },
            success:function(data)
            {
                resp = JSON.parse(data);
                if(resp.status==true)
                {
                    message_display(resp.response, 1);
                    console.log($(this).parent());
                    $('.add_favorite').addClass('remove_favorite_job');
                    $('.add_favorite').removeClass('add_favorite');
                    $('.remove_favorite_job').html('Remove Favorite Job');
                    $('.remove_favorite_job').val('Remove Favorite Job');
                    setTimeout(function(){
                       window.location.reload(1);
                    }, 1000);

                }
            },
            error:function(data)
            {

            }
        }
    )
    return false;
});

$('.remove_favorite_job').on('click', function(event)
{
    event.preventDefault();
    var csrfmdi = document.getElementsByName('csrfmiddlewaretoken')[0].value;
    var id_value = $('.remove_favorite_job').attr('value');
    $.ajax(
        {
            url:'/jobs/remove_favorite_job/',
            type:'POST',
            data:{
                'csrfmiddlewaretoken': csrfmdi,
                'job_id': id_value
            },
            success:function(data)
            {
                resp = JSON.parse(data);
                console.log(resp);
                if(resp.status==true)
                {
                    message_display(resp.response, 1)
                    $(this).removeClass('remove_favorite_job');
                    $(this).addClass('add_favorite');

                    $('.remove_favorite_job').addClass('add_favorite');
                    $('.add_favorite').removeClass('remove_favorite_job');
                    $('.add_favorite').html('Add to Favorite');
                    $('.add_favorite').val('Favorite');
                    setTimeout(function(){
                       window.location.reload(1);
                    }, 1000);


                }
            },
            error:function(data)
            {

            }
        }
    );
    return false;
});

//$('#interview_time, #interview_time_to').bootstrapMaterialDatePicker({
//    date: false,
//    time: true,
//    shortTime: true,
//    format: 'HH:mm'
//});
//$('.interview_date').bootstrapMaterialDatePicker({
//    time: false,
//    format : 'YYYY-MM-DD',
//    minDate : new Date()
//});
//
//
//


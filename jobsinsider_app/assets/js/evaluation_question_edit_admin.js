p/**
 * Created by v on 11/5/15.
 */
var counter = 3;
var selectedans;
$(document).on('click', '.editquestion', function () {
    counter = 3;
  $('#correctanswer').text("");
    $("#heading3").text('');
    $('#option1_id').val('');
    $('#option2_id').val('');
    $('#option3_id').val('');
    $('#option4_id').val('');
    $('#option5_id').val('');


    var question_id=$(this).val();

    $('#admin_idofquestion').val(question_id);
     $.ajax(
        {
            url: '/evaluation/edit/question-options/',
            type: 'GET',
            data:{

                'id':question_id,
                "csrfmiddlewaretoken": document.getElementsByName('csrfmiddlewaretoken')[0].value
            },



            success:function(response)
            {
                console.log(response);
                var data = jQuery.parseJSON(response);
                console.log(data.length);

                value(data.length);

                var data1 = jQuery.parseJSON(data.status);
                 $('#correctanswer').text(data.qesans.answer);

                  console.log(data.length);
                if(data.length==5) {
                    $('#admin_question').val(data.qesans.question);

                    $('#admin_option1').val(data1[0]['fields']['evaluation_question_option']);
                    $('#admin_option1_id').val(data1[0]['pk']);

                    $('#admin_option2').val(data1[1]['fields']['evaluation_question_option']);
                    $('#admin_option2_id').val(data1[1]['pk']);

                    $('#admin_option3').val(data1[2]['fields']['evaluation_question_option']);
                    $('#admin_option3_id').val(data1[2]['pk']);


                    $('#admin_option4').val(data1[3]['fields']['evaluation_question_option']);
                    $('#admin_option4_id').val(data1[3]['pk']);

                    $('#admin_option5').val(data1[4]['fields']['evaluation_question_option']);
                    $('#admin_option5_id').val(data1[4]['pk']);
                }


                if(data.length==4) {
                    $('#admin_question').val(data.qesans.question);

                    $('#admin_option1').val(data1[0]['fields']['evaluation_question_option']);
                    $('#admin_option1_id').val(data1[0]['pk']);

                    $('#admin_option2').val(data1[1]['fields']['evaluation_question_option']);
                    $('#admin_option2_id').val(data1[1]['pk']);

                    $('#admin_option3').val(data1[2]['fields']['evaluation_question_option']);
                    $('#admin_option3_id').val(data1[2]['pk']);


                    $('#admin_option4').val(data1[3]['fields']['evaluation_question_option']);
                    $('#admin_option4_id').val(data1[3]['pk']);

                    $('#admin_option5_id').val('');


                }

                if(data.length==3) {
                    $('#admin_question').val(data.qesans.question);

                    $('#admin_option1').val(data1[0]['fields']['evaluation_question_option']);
                    $('#admin_option1_id').val(data1[0]['pk']);

                    $('#admin_option2').val(data1[1]['fields']['evaluation_question_option']);
                    $('#admin_option2_id').val(data1[1]['pk']);

                    $('#admin_option3').val(data1[2]['fields']['evaluation_question_option']);
                    $('#admin_option3_id').val(data1[2]['pk']);

                    $('#admin_option4_id').val('');
                    $('#admin_option5_id').val('');




                }

                if(data.length==2) {

                    $('#admin_question').val(data.qesans.question);

                    $('#admin_option1').val(data1[0]['fields']['evaluation_question_option']);
                    $('#admin_option1_id').val(data1[0]['pk']);

                    $('#admin_option2').val(data1[1]['fields']['evaluation_question_option']);
                    $('#admin_option2_id').val(data1[1]['pk']);

                    $('#admin_option3_id').val('');
                    $('#admin_option4_id').val('');
                    $('#admin_option5_id').val('');

                }

                if(data.length==1) {
                     $('#admin_question').val(data.qesans.question);

                    $('#admin_option1').val(data1[0]['fields']['evaluation_question_option']);
                    $('#admin_option1_id').val(data1[0]['pk']);

                    $('#admin_option2_id').val('');
                    $('#admin_option3_id').val('');
                    $('#admin_option4_id').val('');
                    $('#admin_option5_id').val('');

                }

                checkanswer=  $('#admin_correctanswer').text();
                if($('#admin_option1').val() == checkanswer||$('#admin_option2').val() == checkanswer||$('#admin_option3').val() == checkanswer||$('#admin_option4').val() == checkanswer||$('#admin_option5').val() == checkanswer){


                }else $('#admin_correctanswer').text('');


            },
            error: function(response) {

        }
        }
    );




    });


$(document).on('change', 'input:radio', function () {

       var selected=$("input[name='radio']:checked").val();
    try {
        if (selected == 1) {

            document.getElementById('admin_option1').style.borderColor = "green";
            selectedans = $('#admin_option1').val();
            $('#admin_correctanswer').text(selectedans);

        } else document.getElementById('admin_option1').style.borderColor = "#DCDCDC";

        if (selected == 2) {

            document.getElementById('admin_option2').style.borderColor = "green";
             selectedans = $('#admin_option2').val();
            $('#admin_correctanswer').text(selectedans);

        } else document.getElementById('admin_option2').style.borderColor = "#DCDCDC";

        if (selected == 3) {
            document.getElementById('admin_option3').style.borderColor = "green";
            selectedans = $('#admin_option3').val();
            $('#admin_correctanswer').text(selectedans);

        } else document.getElementById('admin_option3').style.borderColor = "#DCDCDC";
        if (selected == 4) {

            document.getElementById('admin_option4').style.borderColor = "green";
            selectedans = $('#admin_option4').val();
            $('#admin_correctanswer').text(selectedans);
        } else document.getElementById('admin_option4').style.borderColor = "#DCDCDC";
        if (selected == 5) {

            document.getElementById('admin_option5').style.borderColor = "green";
            selectedans = $('#admin_option5').val();
            $('#admin_correctanswer').text(selectedans);
        } else document.getElementById('admin_option5').style.borderColor = "#DCDCDC";
    } catch(err){


    }

    });
$(document).on('click', '#reset', function () {
try {
    $('#admin_question').val("");
    $('#admin_correct_answer').val("");
    $('#admin_option1').val("");
    $('#admin_option2').val("");
    $('#admin_option3').val("");
    $('#admin_option4').val("");
    $('#admin_option5').val("");
    $("#box" + 3).remove();
    $("#box" + 4).remove();
    $("#box" + 5).remove();
    $("#label" + 3).remove();
    $("#label" + 4).remove();
    $("#label" + 5).remove();
    $('#correctanswer').text("");
    document.getElementById('admin_option1').style.borderColor = "#DCDCDC";
    document.getElementById('admin_option2').style.borderColor = "#DCDCDC";
    document.getElementById('admin_option3').style.borderColor = "#DCDCDC";
    document.getElementById('admin_option4').style.borderColor = "#DCDCDC";
    document.getElementById('admin_option5').style.borderColor = "#DCDCDC";

} catch(Err){


}

});

$('#neweditmodal').ready(function(){



    $("#admin_addoptions").click(function () {
        $("#heading3").text("").show();




	if(counter>5){
            $("#heading3").text("Not more than 5 options").delay(2000).fadeOut();
            return false;
	}

	var newTextBoxDiv = $(document.createElement('div'))
	     .attr("class", 'form-group').attr("id","admin_box" + counter);


        var text='<input type="text" class = "form-control" " name="option' + counter +
	      '" id="admin_option' + counter + '" value="" placeholder = "option">'

        var label='<label class = "col-sm-2 control-label">Option ' + counter + '</label>' + '<div class ="col-sm-10">'+ text +'</div>';

         var radio='<label id="admin_label'+counter+'" class="btn btn-default">'+
               '<input type="radio" name="radio" id="radio' + counter +' " value="'+counter +'"> Option  ' + counter + '</label>';

        newTextBoxDiv.before().html(label);


        $( "#admin_inserthere" ).append( $(radio) );
     $( "#admin_lastchild" ).first().before( newTextBoxDiv );








	counter++;
     });

     $("#admin_removeoptions").click(function () {
         $("#heading3").text("").show();




	   if(counter==3){
          $("#heading3").text("Min options are 2").delay(2000).fadeOut();
          return false;
       }

	counter--;



         id=$("#admin_option"+ counter +"_id").val();
         event.preventDefault();
      $.ajax(
        {
            url: '/evaluation/edit/question-options/delete/',
            type: 'GET',
            data:{
                'id':id,
                "csrfmiddlewaretoken": document.getElementsByName('csrfmiddlewaretoken')[0].value
            },



            success:function(response)
            {



            },
            error: function(response) {

        }
        }
    );














        $("#admin_box" + counter).remove();
         $("#admin_label" + counter).remove();


     });

  });


function value(data){

    if(data == 3){
        counter=3;
                    try {
                        $("#admin_box" + 3).remove();
                        $("#admin_label" + 3).remove();
                        $("#admin_box" + 4).remove();
                        $("#admin_label" + 4).remove();
                         $("#admin_box" + 5).remove();
                        $("#admin_label" + 5).remove();
                    }
                    catch(e){

                    }

                    var newTextBoxDiv = $(document.createElement('div'))
	                 .attr("class", 'form-group').attr("id","admin_box" + counter);


                  var text='<input type="text" class = "form-control" " name="option' + counter +
	             '" id="admin_option' + counter + '" value="" placeholder = "option">'

                 var label='<label class = "col-sm-2 control-label">Option ' + counter + '</label>' + '<div class ="col-sm-10">'+ text +'</div>';

                  var radio='<label id="admin_label'+counter+'" class="btn btn-default">'+
                  '<input type="radio" name="radio" id="radio' + counter +' " value="'+counter +'"> Option  ' + counter + '</label>';

                        newTextBoxDiv.before().html(label);


                       $( "#admin_inserthere" ).append( $(radio) );
                      $( "#admin_lastchild" ).first().before( newTextBoxDiv );
                    counter++;
                }



                if(data == 4){
                    counter=3;

                    try {
                        $("#admin_box" + 3).remove();
                        $("#admin_label" + 3).remove();
                        $("#admin_box" + 4).remove();
                        $("#admin_label" + 4).remove();
                         $("#admin_box" + 5).remove();
                        $("#admin_label" + 5).remove();
                    }
                    catch(e){

                    }


                      for(i=0;i<2;i++) {
                      var newTextBoxDiv = $(document.createElement('div'))
                          .attr("class", 'form-group').attr("id", "admin_box" + counter);


                      var text = '<input type="text" class = "form-control" " name="option' + counter +
                          '" id="admin_option' + counter + '" value="" placeholder = "option">'

                      var label = '<label class = "col-sm-2 control-label">Option ' + counter + '</label>' + '<div class ="col-sm-10">' + text + '</div>';

                      var radio = '<label id="admin_label' + counter + '" class="btn btn-default">' +
                          '<input type="radio" name="radio" id="radio' + counter + ' " value="' + counter + '" autocomplete="off"> Option  ' + counter + '</label>';

                      newTextBoxDiv.before().html(label);


                      $("#admin_inserthere").append($(radio));
                      $("#admin_lastchild").first().before(newTextBoxDiv);
                      counter++;


                  }
                }





     if(data == 5){
                    counter=3;

                    try {
                        $("#admin_box" + 3).remove();
                        $("#admin_label" + 3).remove();
                        $("#admin_box" + 4).remove();
                        $("#admin_label" + 4).remove();
                         $("#admin_box" + 5).remove();
                        $("#admin_label" + 5).remove();
                    }
                    catch(e){

                    }


                      for(i=0;i<3;i++) {
                      var newTextBoxDiv = $(document.createElement('div'))
                          .attr("class", 'form-group').attr("id", "admin_box" + counter);


                      var text = '<input type="text" class = "form-control" " name="option' + counter +
                          '" id="admin_option' + counter + '" value="" placeholder = "option">'

                      var label = '<label class = "col-sm-2 control-label">Option ' + counter + '</label>' + '<div class ="col-sm-10">' + text + '</div>';

                      var radio = '<label id="admin_label' + counter + '" class="btn btn-default">' +
                          '<input type="radio" name="radio" id="radio' + counter + ' " value="' + counter + '" autocomplete="off"> Option  ' + counter + '</label>';

                      newTextBoxDiv.before().html(label);


                      $("#admin_inserthere").append($(radio));
                      $("#admin_lastchild").first().before(newTextBoxDiv);
                      counter++;


                  }
                }

}
var optioncount;
$(document).on('click', '#update_question_button', function () {
    optioncount=0;

     $("#heading3").text('');
    $('#answerofquestion').val($('#admin_correctanswer').text());

     if($('#admin_option1').val()) {
         optioncount++;
     }
    if($('#admin_option2').val()) {
         optioncount++;
     }
    if($('#admin_option3').val()) {
         optioncount++;
     }
    if($('#admin_option4').val()) {
         optioncount++;
     }
    if($('#admin_option5').val()) {
         optioncount++;
     }
event.preventDefault();
    if(optioncount>=2){




     event.preventDefault();

    if($('#correctanswer').text()) {
        $("#heading3").text('');
        event.preventDefault();
        $.ajax(
            {
                url: '/evaluation/edit/question-options/',
                type: 'POST',
                data: $('form#update_question').serialize(),


                success: function (response) {
                    var data = jQuery.parseJSON(response);
                    if (data.status == "True") {

                        $("#heading3").text('Updated').delay(2000).fadeOut();


                    }


                },
                error: function (response) {

                }
            }
        );


    } else $("#heading3").text('Choose Answer').delay(2000).fadeOut();






    } else $("#heading3").text('Enter At least 2 options').delay(2000).fadeOut();
















    });


$(document).on('click', '.delete', function () {

    id=$(this).val();
     event.preventDefault();
    $(this).closest('tr').remove().delay(2000).fadeOut();
      $.ajax(
        {
            url: '/evaluation/edit/question-options/delete/',
            type: 'POST',
            data:{
                'id':id,
                "csrfmiddlewaretoken": document.getElementsByName('csrfmiddlewaretoken')[0].value
            },



            success:function(response)
            {
                var data = jQuery.parseJSON(response);
                if (data.status == "True") {




                    }




            },
            error: function(response) {

        }
        }
    );




    });
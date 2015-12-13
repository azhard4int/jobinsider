/**
 * Created by v on 11/5/15.
 */
var counter = 3;
var selectedans;
$(document).on('click', '.uf_editquestion', function () {
    counter = 3;



  $('#correctanswer').text("");
    $("#heading3").text('');
    $('#option1_id').val('');
    $('#option2_id').val('');
    $('#option3_id').val('');
    $('#option4_id').val('');
    $('#option5_id').val('');





    var question_id=$(this).val();
    $('#uf_idofquestion').val(question_id);

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
              var data = jQuery.parseJSON(response);


                value(data.length);

                var data1 = jQuery.parseJSON(data.status);
                 $('#correctanswer').text(data.qesans.answer);

                  console.log(data.length);
                if(data.length==5) {
                    $('#question').val(data.qesans.question);

                    $('#option1').val(data1[0]['fields']['evaluation_question_option']);
                    $('#option1_id').val(data1[0]['pk']);

                    $('#option2').val(data1[1]['fields']['evaluation_question_option']);
                    $('#option2_id').val(data1[1]['pk']);

                    $('#option3').val(data1[2]['fields']['evaluation_question_option']);
                    $('#option3_id').val(data1[2]['pk']);


                    $('#option4').val(data1[3]['fields']['evaluation_question_option']);
                    $('#option4_id').val(data1[3]['pk']);

                    $('#option5').val(data1[4]['fields']['evaluation_question_option']);
                    $('#option5_id').val(data1[4]['pk']);
                }


                if(data.length==4) {
                    $('#question').val(data.qesans.question);

                    $('#option1').val(data1[0]['fields']['evaluation_question_option']);
                    $('#option1_id').val(data1[0]['pk']);

                    $('#option2').val(data1[1]['fields']['evaluation_question_option']);
                    $('#option2_id').val(data1[1]['pk']);

                    $('#option3').val(data1[2]['fields']['evaluation_question_option']);
                    $('#option3_id').val(data1[2]['pk']);


                    $('#option4').val(data1[3]['fields']['evaluation_question_option']);
                    $('#option4_id').val(data1[3]['pk']);

                    $('#option5_id').val('');


                }

                if(data.length==3) {
                    $('#question').val(data.qesans.question);

                    $('#option1').val(data1[0]['fields']['evaluation_question_option']);
                    $('#option1_id').val(data1[0]['pk']);

                    $('#option2').val(data1[1]['fields']['evaluation_question_option']);
                    $('#option2_id').val(data1[1]['pk']);

                    $('#option3').val(data1[2]['fields']['evaluation_question_option']);
                    $('#option3_id').val(data1[2]['pk']);

                    $('#option4_id').val('');
                    $('#option5_id').val('');




                }

                if(data.length==2) {
                     $('#question').val(data.qesans.question);

                    $('#option1').val(data1[0]['fields']['evaluation_question_option']);
                    $('#option1_id').val(data1[0]['pk']);

                    $('#option2').val(data1[1]['fields']['evaluation_question_option']);
                    $('#option2_id').val(data1[1]['pk']);

                    $('#option3_id').val('');
                    $('#option4_id').val('');
                    $('#option5_id').val('');


                }

                if(data.length==1) {
                     $('#question').val(data.qesans.question);

                    $('#option1').val(data1[0]['fields']['evaluation_question_option']);
                    $('#option1_id').val(data1[0]['pk']);

                    $('#option2_id').val('');
                    $('#option3_id').val('');
                    $('#option4_id').val('');
                    $('#option5_id').val('');

                }

                checkanswer= $('#correctanswer').text();
                if($('#option1').val() == checkanswer||$('#option2').val() == checkanswer||$('#option3').val() == checkanswer||$('#option4').val() == checkanswer||$('#option5').val() == checkanswer){


                }else $('#correctanswer').text('');


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

            document.getElementById('option1').style.borderColor = "green";
            selectedans = $('#option1').val();
            $('#correctanswer').text(selectedans);

        } else document.getElementById('option1').style.borderColor = "#DCDCDC";

        if (selected == 2) {

            document.getElementById('option2').style.borderColor = "green";
             selectedans = $('#option2').val();
            $('#correctanswer').text(selectedans);

        } else document.getElementById('option2').style.borderColor = "#DCDCDC";

        if (selected == 3) {
            document.getElementById('option3').style.borderColor = "green";
            selectedans = $('#option3').val();
            $('#correctanswer').text(selectedans);

        } else document.getElementById('option3').style.borderColor = "#DCDCDC";
        if (selected == 4) {

            document.getElementById('option4').style.borderColor = "green";
            selectedans = $('#option4').val();
            $('#correctanswer').text(selectedans);
        } else document.getElementById('option4').style.borderColor = "#DCDCDC";
        if (selected == 5) {

            document.getElementById('option5').style.borderColor = "green";
            selectedans = $('#option5').val();
            $('#correctanswer').text(selectedans);
        } else document.getElementById('option5').style.borderColor = "#DCDCDC";
    } catch(err){


    }

    });
$(document).on('click', '#reset', function () {
try {
    $('#question').val("");
    $('#correct_answer').val("");
    $('#option1').val("");
    $('#option2').val("");
    $('#option3').val("");
    $('#option4').val("");
    $('#option5').val("");
    $("#box" + 3).remove();
    $("#box" + 4).remove();
    $("#box" + 5).remove();
    $("#label" + 3).remove();
    $("#label" + 4).remove();
    $("#label" + 5).remove();
    $('#correctanswer').text("");
    document.getElementById('option1').style.borderColor = "#DCDCDC";
    document.getElementById('option2').style.borderColor = "#DCDCDC";
    document.getElementById('option3').style.borderColor = "#DCDCDC";
    document.getElementById('option4').style.borderColor = "#DCDCDC";
    document.getElementById('option5').style.borderColor = "#DCDCDC";

} catch(Err){


}

});

$('#neweditmodal').ready(function(){



    $("#uf_addoptions").click(function () {
        $("#heading3").text("").show();




	if(counter>5){
            $("#heading3").text("Not more than 5 options").delay(2000).fadeOut();
            return false;
	}

	var newTextBoxDiv = $(document.createElement('div'))
	     .attr("class", 'form-group').attr("id","box" + counter);


        var text='<input type="text" class = "form-control" " name="option' + counter +
	      '" id="option' + counter + '" value="" placeholder = "option">'

        var label='<label class = "col-sm-2 control-label">Option ' + counter + '</label>' + '<div class ="col-sm-10">'+ text +'</div>';

         var radio='<label id="label'+counter+'" class="btn btn-default">'+
               '<input type="radio" name="radio" id="radio' + counter +' " value="'+counter +'"> Option  ' + counter + '</label>';

        newTextBoxDiv.before().html(label);


        $( "#uf_inserthere" ).append( $(radio) );
     $( "#uf_lastchild" ).first().before( newTextBoxDiv );








	counter++;
     });

     $("#uf_removeoptions").click(function () {
         $("#heading3").text("").show();




	   if(counter==3){
          $("#heading3").text("Min options are 2").delay(2000).fadeOut();
          return false;
       }

	counter--;



         id=$("#option"+ counter +"_id").val();
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














        $("#box" + counter).remove();
         $("#label" + counter).remove();


     });

  });


function value(data){

    if(data == 3){
        counter=3;
                    try {
                        $("#box" + 3).remove();
                        $("#label" + 3).remove();
                        $("#box" + 4).remove();
                        $("#label" + 4).remove();
                         $("#box" + 5).remove();
                        $("#label" + 5).remove();
                    }
                    catch(e){

                    }

                    var newTextBoxDiv = $(document.createElement('div'))
	                 .attr("class", 'form-group').attr("id","box" + counter);


                  var text='<input type="text" class = "form-control" " name="option' + counter +
	             '" id="option' + counter + '" value="" placeholder = "option">'

                 var label='<label class = "col-sm-2 control-label">Option ' + counter + '</label>' + '<div class ="col-sm-10">'+ text +'</div>';

                  var radio='<label id="label'+counter+'" class="btn btn-default">'+
                  '<input type="radio" name="radio" id="radio' + counter +' " value="'+counter +'"> Option  ' + counter + '</label>';

                        newTextBoxDiv.before().html(label);


                       $( "#uf_inserthere" ).append( $(radio) );
                      $( "#uf_lastchild" ).first().before( newTextBoxDiv );
                    counter++;
                }



                if(data == 4){
                    counter=3;

                    try {
                        $("#box" + 3).remove();
                        $("#label" + 3).remove();
                        $("#box" + 4).remove();
                        $("#label" + 4).remove();
                         $("#box" + 5).remove();
                        $("#label" + 5).remove();
                    }
                    catch(e){

                    }


                      for(i=0;i<2;i++) {
                      var newTextBoxDiv = $(document.createElement('div'))
                          .attr("class", 'form-group').attr("id", "box" + counter);


                      var text = '<input type="text" class = "form-control" " name="option' + counter +
                          '" id="option' + counter + '" value="" placeholder = "option">'

                      var label = '<label class = "col-sm-2 control-label">Option ' + counter + '</label>' + '<div class ="col-sm-10">' + text + '</div>';

                      var radio = '<label id="label' + counter + '" class="btn btn-default">' +
                          '<input type="radio" name="radio" id="radio' + counter + ' " value="' + counter + '" autocomplete="off"> Option  ' + counter + '</label>';

                      newTextBoxDiv.before().html(label);


                      $("#uf_inserthere").append($(radio));
                      $("#uf_lastchild").first().before(newTextBoxDiv);
                      counter++;


                  }
                }





     if(data == 5){
                    counter=3;

                    try {
                        $("#box" + 3).remove();
                        $("#label" + 3).remove();
                        $("#box" + 4).remove();
                        $("#label" + 4).remove();
                         $("#box" + 5).remove();
                        $("#label" + 5).remove();
                    }
                    catch(e){

                    }


                      for(i=0;i<3;i++) {
                      var newTextBoxDiv = $(document.createElement('div'))
                          .attr("class", 'form-group').attr("id", "box" + counter);


                      var text = '<input type="text" class = "form-control" " name="option' + counter +
                          '" id="option' + counter + '" value="" placeholder = "option">'

                      var label = '<label class = "col-sm-2 control-label">Option ' + counter + '</label>' + '<div class ="col-sm-10">' + text + '</div>';

                      var radio = '<label id="label' + counter + '" class="btn btn-default">' +
                          '<input type="radio" name="radio" id="radio' + counter + ' " value="' + counter + '" autocomplete="off"> Option  ' + counter + '</label>';

                      newTextBoxDiv.before().html(label);


                      $("#uf_inserthere").append($(radio));
                      $("#uf_lastchild").first().before(newTextBoxDiv);
                      counter++;


                  }
                }

}
var optioncount;
$(document).on('click', '#update_question_button', function () {
    optioncount=0;

     $("#heading3").text('');
    $('#answerofquestion').val($('#correctanswer').text());

     if($('#option1').val()) {
         optioncount++;
     }
    if($('#option2').val()) {
         optioncount++;
     }
    if($('#option3').val()) {
         optioncount++;
     }
    if($('#option4').val()) {
         optioncount++;
     }
    if($('#option5').val()) {
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
                data: $('form#uf_update_question').serialize(),


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


$(document).on('click', '.uf_delete', function () {

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
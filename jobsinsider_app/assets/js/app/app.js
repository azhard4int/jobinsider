/**
 * Created by azhar on 10/1/15.
 */

var base_url = 'http://jobinsider.xyz:8000/';
var app = angular.module('filtersapp', []);
//custom tag settings
app.config(function($interpolateProvider) {
  $interpolateProvider.startSymbol('<<');
  $interpolateProvider.endSymbol('>>');
});
app.controller('rootCtrl', function($http, $scope)
{
    $scope.categories_id = [];
    $scope.employment_id = [];
    $scope.experience_id = [];
    $scope.education_id = [];



});
app.controller('leftfilters', function($http, $scope)
{
    $scope.categories = [];
    $scope.experience = [];
    $scope.employment = [];
    $scope.countries = [];
    $scope.education = [];
    $scope.cities = [];
    $scope.is_categories=true;
    $scope.is_experience=true;
    $scope.is_education=true;
    $scope.is_employment = true;
    $scope.counter_categories = 0;
    $scope.counter_experience = 0;
    $scope.counter_education = 0;
    $scope.counter_employment = 0;
    $http(
        {
            method: 'GET',
            url: base_url + 'api/categories/'
        }
    ).success(function(data)
            {
                var value = angular.fromJson(data);
                $scope.categories = value;
            });
    //fetch experience type
    $http(
        {
            method: 'GET',
            url: base_url + 'api/experience/'
        }
    ).success(function(data)
            {
                var value = angular.fromJson(data);
                $scope.experience = value;
            });
    //fetch education type
    $http(
        {
            method: 'GET',
            url: base_url + 'api/education/'
        }
    ).success(function(data)
            {
                var value = angular.fromJson(data);
                $scope.education = value;
            });
    //fetch employment type
    $http(
        {
            method: 'GET',
            url: base_url + 'api/employment/'
        }
    ).success(function(data)
            {
                var value = angular.fromJson(data);
                $scope.employment = value;
            });
    $scope.isCategories = function()
    {
        if($scope.counter_categories==0)
        {
            this.is_categories = false;
            $scope.counter_categories++;
        }
        else{
            this.is_categories = true;
            $scope.counter_categories = 0;

        }

    };
    $scope.isExperience = function()
    {
        if($scope.counter_experience==0)
        {
            this.is_experience = false;
            $scope.counter_experience++;
        }
        else{
            this.is_experience = true;
            $scope.counter_experience = 0;

        }

    };

    $scope.isEducation = function()
    {
        if($scope.counter_education==0)
        {
            this.is_education = false;
            $scope.counter_education++;
        }
        else{
            this.is_education = true;
            $scope.counter_education = 0;

        }

    };
    $scope.isEmployment = function()
    {
        if($scope.counter_employment==0)
        {
            this.is_employment = false;
            $scope.counter_employment++;
        }
        else{
            this.is_employment = true;
            $scope.counter_employment = 0;

        }

    };


    $scope.categoriesInsert = function(value)
    {
        if(this.categoriesID[value])
        {
            this.categories_id.push(value);
            this.getfilteredResults();
        }
        else{

            this.categories_id.pop(value);
             this.getfilteredResults();
        }

    };
    $scope.employmentInsert = function(value)
    {
        if(this.employmentID[value])
        {
            this.employment_id.push(value);
            this.getfilteredResults();
        }
        else{
            this.employment_id.pop(value);
            this.getfilteredResults();
        }

    };
    $scope.experienceInsert = function(value)
    {
        if(this.experienceID[value])
        {
            this.experience_id.push(value);
            this.getfilteredResults();
        }
        else{
            this.experience_id.pop(value);
            this.getfilteredResults();
        }

    };
    $scope.educationInsert = function(value)
    {
        if(this.educationID[value])
        {
            this.education_id.push(value);
            this.getfilteredResults();


        }
        else{
            this.education_id.pop(value);
            this.getfilteredResults();
        }

    };


    $scope.getfilteredResults = function()
    {
        var search_keyword = $('.search_keyword').val();
        if(search_keyword=='')
        {
            url_to =  base_url + 'jobs/filtered/?categories='+this.categories_id+"&experience="+ this.experience_id +"&is_ajax=1" +
                    "&education="+ this.education_id+"&employment="+ this.employment_id
        }
        else{
            url_to =  base_url + 'jobs/filtered/?categories='+this.categories_id+"&experience="+ this.experience_id +"&is_ajax=1" +
                    "&education="+ this.education_id+"&employment="+ this.employment_id+"&search="+search_keyword
        }

        $http(
              {
                'method':'GET',
                'url':url_to
            }
        ).success(function(data)
              {
                  $('.jobsearch_right_filter').html(data);
                  console.log(data)
              })
    };



});

app.controller('paginationCtrl', function($http, $scope)
{
   //update the jobs results

    $scope.getResults = function(pageValue)
    {
        console.log(pageValue);
        $http(
              {
                'method':'GET',
                'url': base_url + 'jobs/index/?page='+pageValue+"&is_ajax=1"
            }
        ).success(function(data)
              {
                  $('.jobsearch_right_filter').html(data);
                  console.log(data)
              })

    };

    $scope.getFilteredPaginate = function(value)
    {
        $http(
              {
                'method':'GET',
                //'url': base_url + 'jobs/filtered/?categories='+this.categories_id+"&is_ajax=1&page="+value
                'url': base_url + 'jobs/filtered/?categories='+this.categories_id+"&is_ajax=1&page="+value+ "&experience="+
                this.experience_id +"&is_ajax=1" + "&education="+ this.education_id+"&employment="+ this.employment_id
            }
        ).success(function(data)
              {
                  $('.jobsearch_right_filter').html(data);
                  console.log(data)
              })
    };
});

function getResults(pageValue)
{
    //console.log(value);
    //getting data attributes
    var categories = $('.data_attribute_get').data('categories');
    var experience = $('.data_attribute_get').data('experience');
    var employment = $('.data_attribute_get').data('employment');
    var education = $('.data_attribute_get').data('education');
    console.log(education);
    if(categories==undefined)
    {
        categories='';
    }
    if(experience==undefined)
    {
        experience='';
    }
    if(employment==undefined)
    {
        employment='';
    }
    if(education==undefined)
    {
        education='';
    }
    var search_keyword = $('.search_keyword').val();
    if (search_keyword=='')
    {
        url = base_url + 'jobs/filtered/?categories='+categories+"&is_ajax=1&page="+pageValue+ "&experience="+
                experience +"&is_ajax=1" + "&education="+ education + "&employment="+ employment
    }
    else{
         url = base_url + 'jobs/filtered/?categories='+categories+"&is_ajax=1&page="+pageValue+ "&experience="+
                experience +"&is_ajax=1" + "&education="+ education + "&employment="+ employment +"&search="+search_keyword
    }
    $.ajax({
            'method':'GET',
            //'url': base_url + 'jobs/index/?page='+pageValue+"&is_ajax=1",
            'url': url,
            success: function(data)
              {
                  $('.jobsearch_right_filter').html(data);
                  console.log(data)
              }
            }
        )

};

$('.search_button').on('click', function(e)
{
    e.preventDefault();
    var categories = $('.data_attribute_get').data('categories');
    var experience = $('.data_attribute_get').data('experience');
    var employment = $('.data_attribute_get').data('employment');
    var education = $('.data_attribute_get').data('education');
    console.log(education);
    if(categories==undefined)
    {
        categories='';
    }
    if(experience==undefined)
    {
        experience='';
    }
    if(employment==undefined)
    {
        employment='';
    }
    if(education==undefined)
    {
        education='';
    }
    var search_keyword = $('.search_keyword').val();
    var pageValue = $('.data_attribute_get').data('pagevalue');
    if(pageValue==undefined)
    {
        pageValue=1;
    }
    url = base_url + 'jobs/filtered/?categories='+categories+"&is_ajax=1&page="+pageValue+ "&experience="+
                experience +"&is_ajax=1" + "&education="+ education + "&employment="+ employment+ "&search="+search_keyword
    $.ajax({
            'method':'GET',
            //'url': base_url + 'jobs/index/?page='+pageValue+"&is_ajax=1",
            'url': url,
            success: function(data)
              {
                  $('.jobsearch_right_filter').html(data);
                  console.log(data)
              }
            }
        )

    return false;
});


function get_user_applied(pageValue)
{
    //console.log(value);
    //getting data attributes

    $.ajax({
            'method':'GET',
            'url': base_url + 'jobs/applied/?page='+pageValue+"&is_ajax=1",
            //'url': url,
            success: function(data)
              {
                  $('.jobsearch_right_filter').html(data);
                  console.log(data)
              }
            }
        )

};

function get_user_favorite(pageValue)
{
    //console.log(value);
    //getting data attributes

    $.ajax({
            'method':'GET',
            'url': base_url + 'jobs/favorite/?page='+pageValue+"&is_ajax=1",
            //'url': url,
            success: function(data)
              {
                  $('.jobsearch_right_filter').html(data);
                  console.log(data)
              }
            }
        )

};
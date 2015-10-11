/**
 * Created by azhar on 10/1/15.
 */

var base_url = 'http://127.0.0.1:8000/';
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
    $scope.is_categories = false;
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
        this.is_categories = true;
    };
    $scope.categoriesInsert = function(value)
    {
        if(this.categoriesID[value])
        {
            this.categories_id.push(value);
            alert(this.categories_id)
            this.getfilteredResults(this.categories_id);
        }
        else{
            this.categories_id.pop(value);
        }

    };
    $scope.employmentInsert = function(value)
    {
        if(this.employmentID[value])
        {
            this.employment_id.push(value);
            alert(this.employment_id)

        }
        else{
            this.employment_id.pop(value);
        }

    };
    $scope.experienceInsert = function(value)
    {
        if(this.experienceID[value])
        {
            this.experience_id.push(value);
            alert(this.experience_id)

        }
        else{
            this.experience_id.pop(value);
        }

    };
    $scope.educationInsert = function(value)
    {
        if(this.educationID[value])
        {
            this.education_id.push(value);
            alert(this.education_id)

        }
        else{
            this.education_id.pop(value);
        }

    };


    $scope.getfilteredResults = function(categories)
    {
        console.log(categories);
        $http(
              {
                'method':'GET',
                'url': base_url + 'jobs/filtered/?categories='+categories+"&is_ajax=1"
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
        alert('awesome');
        $http(
              {
                'method':'GET',
                'url': base_url + 'jobs/filtered/?categories='+this.categories_id+"&is_ajax=1&page="+value
            }
        ).success(function(data)
              {
                  $('.jobsearch_right_filter').html(data);
                  console.log(data)
              })
    };
});
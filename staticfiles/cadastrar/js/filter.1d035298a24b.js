$(document).ready(function() {
    $("#searchTitular").on("keyup", function() {
      var value = $(this).val().toLowerCase();
      $("#idListVit tbody tr").filter(function() {
        $(this).toggle($(this).find("td:nth-child(3)").text().toLowerCase().indexOf(value) > -1)
      });
    });
  });
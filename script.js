$(document).ready(function()
{
  $('#navigation li').click(function()
  {
    $(this).siblings().each(function()
    {
      $(this).removeClass('selected');
      $('#' + $(this).text().toLowerCase().replace(' ', '_')).hide();
    });
    
    $(this).addClass('selected');
    $('#' + $(this).text().toLowerCase().replace(' ', '_')).show();
  });
  
  $('#navigation li:eq(2)').trigger('click');
});

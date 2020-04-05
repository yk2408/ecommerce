$(document).ready(function()
      {
          $('#subscribe').click(function(e)
          {
            e.preventDefault();
            var email_id = $('#id_email').val();
            console.log(email_id)
            if(email_id)
            {
            var csrfmiddlewaretoken = csrftoken;
            var subscribe_url = $(this).attr('url');
            var email_data ={ 'email': email_id,
                              'status': 'subscribed',
                              'csrfmiddlewaretoken': csrfmiddlewaretoken
                              };
            $.ajax({
                    type: 'POST',
                    url: subscribe_url,
                    data: email_data,
                    success: function(response)
                    {
                        $('#id_email').val('');
                        if(response.status == '404' || response.status == 400 )
                        {

                            var html = "<span class='error' style='color: red;'>"+ response.msg +"</span>";
                            $(".response-msg").html(html);

                        }
                        else
                        {
                            var html = "<span class='success' style='color: green;'>Thank you for Subscribing! Please Check your Email to Confirm the Subscription</span>";
                            $(".response-msg").html(html);
                        }

                    },
                    error: function(response)
                    {
                        alert('Sorry Something Went Wrong');
                        $('#id_email').val('');
                    }
                  });
                  return false;
            }
            else
            {
                alert('Please Provide Correct Email')
            }
          });
          function manage_cart_wish(add_url)
          {
            $.ajax
            ({
                type: "GET",
                url: add_url,
                success: function(result)
                {
                  if(result.authenticated == false) 
                  {
                    current_url = $(location).attr('href')
                    window.location.href = "/userprofile/login/?next="+ current_url
                  }
                  else
                  {
                    if(result.status == "Already")
                    {
                        alert("already add in wishlist")
                    }
                    else
                    {
                        window.location.reload();
                    }
                  }
                }
            });
          };
          $(".add-cart").click(function(event)
          {
            var cart_url = $(this).attr("url");
            console.log(cart_url);
            manage_cart_wish(cart_url);
          });
          $(".w-list").click(function(event)
          {
            var wish_url = $(this).attr("url");
            manage_cart_wish(wish_url);
          });
          function manage_qty(qty, product_name)
          {
            if(qty=="inc")
            {
                var inc = 1
            }
            else
            {
              if(qty == "dec")
              {
                var inc = -1
              }
              else
              {
                var inc = 0
              }
            }
            var csrfmiddlewaretoken = csrftoken;
            var inc_data ={'inc': inc,
                           'product_name':product_name,
                           'csrfmiddlewaretoken': csrfmiddlewaretoken
                              };
            $.ajax
            ({
                type: "POST",
                data: inc_data,
                url: "/cart/mycart/",
                success: function(result)
                {
                    window.location.reload();

                }
            });
          };
          $(".inc.qtybutton").click(function(e)
          {
            var product_name = $(this).attr("name");
            manage_qty("inc", product_name);
          });
          $(".dec.qtybutton").click(function(e)
          {
            var product_name = $(this).attr("name");
            //alert(product_name);
            var decr = $(this).next(".cart-plus-minus-box").attr("value")
            if(decr == 1)
              { 
                manage_qty("zero", product_name);
              }
            else
              {
                manage_qty("dec", product_name);  
              }
            
          });

          $(".rmv").click(function(event)
          {
            var remove_wish_url = $(this).attr('url');
            console.log(remove_wish_url)
            $.ajax(
            {
                type:"POST",
                url: remove_wish_url,
                success: function(result)
                {
                    window.location.reload();
                    
                }
            });
          });

          $('#post-form').submit(function() 
          { 
            alert($(this).serialize());
            $.ajax(
            { 
                data: $(this).serialize(), // get the form data
                type: $(this).attr('method'), // GET or POST
                url: $(this).attr('action'), // the file to call
                success: function(response) 
                { 
                   if(response.data == "success")
                   {
                      window.location.reload();
                   }          
                }
            });
            return false;
          });
          $('#add-form').submit(function() 
          { 
            $.ajax(
            { 
                data: $(this).serialize(), // get the form data
                type: $(this).attr('method'), // GET or POST
                url: $(this).attr('action'), // the file to call
                success: function(response) 
                { 
                   if(response.data == "success")
                   {
                      window.location.reload();
                   }          
                }
            });
            return false;
          });
          $(".delete-address").click(function(event)
          {
            var delete_url = $(this).attr('url');
            var r = confirm("Are you sure you want to delete address");
            console.log(r)
            if (r == true)
            {
              console.log(r)
                $.ajax(
                {
                    type:"POST",
                    url: delete_url,
                    success: function(result)
                    {
                        window.location.reload();
                    }
                });
            }

          });

          $(".delivery-manage").click(function()
          {
            var address_id = $(this).attr('address_id');
            if(address_id == address)
            $("#add-de").hide();
              
          });  
          
          var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();

          function csrfSafeMethod(method)
            {
                return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
            }
          $.ajaxSetup(
          {
            beforeSend: function(xhr, settings)
            {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain)
                {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            }
          });
      });
window.drf = {
  csrfHeaderName: "X-CSRFTOKEN",
  csrfCookieName: "csrftoken"
};

$(document).ready(function () {
    var csrftoken = getCookie(window.drf.csrfCookieName);
    $.ajaxSetup({
      beforeSend: function (xhr, settings) {
          if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
              // Send the token to same-origin, relative URLs only.
              // Send the token only if the method warrants CSRF protection
              // Using the CSRFToken value acquired earlier
              xhr.setRequestHeader(window.drf.csrfHeaderName, csrftoken);
          }
      }
      
    });
    $(".widgets_div.addcustomermenu").click(function () {
        $(".viewlist").addClass("deactive");
        $(".viewlist.addcustomerview").removeClass("deactive");
    });
    $(".widgets_div.invoicemenu").click(function () {
        $(".viewlist").addClass("deactive");
        $(".viewlist.invoiceview").removeClass("deactive");
    });
    $(".widgets_div.analyticsmenu").click(function () {
        $(".viewlist").addClass("deactive");
        $(".viewlist.analyticsview").removeClass("deactive");
    });
    $(".widgets_div.myactivitymenu").click(function () {
        $(".viewlist").addClass("deactive");
        $(".viewlist.myactivityview").removeClass("deactive");
    });
    $(".widgets_div.transactionmenu").click(function () {
        $(".viewlist").addClass("deactive");
        $(".viewlist.transactionview").removeClass("deactive");
    });
    $(".widgets_div.settingsmenu").click(function () {
        $(".viewlist").addClass("deactive");
        $(".viewlist.settingsview").removeClass("deactive");
    });
    $(".widgets_div.helpmenu").click(function () {
        $(".viewlist").addClass("deactive");
        $(".viewlist.helpview").removeClass("deactive");
    });

    $("img#profile-image").click(function () {
        if ($(".profile-menus").hasClass("deactive")) {
            $(".profile-menus").addClass("active");
            $(".profile-menus").removeClass("deactive");
            $("#myprofile").click(function (e) {
                $(".viewlist").addClass("deactive");
                $(".viewlist.myprofileview").removeClass("deactive");
                $(".profile-menus").addClass("deactive");
                $(".profile-menus").removeClass("active");
            });

            $("#profilesettings").click(function (e) {
                $(".viewlist").addClass("deactive");
                $(".viewlist.mysettingview").removeClass("deactive");
                $(".profile-menus").addClass("deactive");
                $(".profile-menus").removeClass("active");
            });
        } else {
            $(".profile-menus").addClass("deactive");
            $(".profile-menus").removeClass("active");
        }
    });

});

// drop-down for js
var a = {
    Cars: [{
        "CarType": "BMW",
        "carID": "bmw123"
    }, {
        "CarType": "mercedes",
        "carID": "merc123"
    }, {
        "CarType": "volvo",
        "carID": "vol123r"
    }, {
        "CarType": "ford",
        "carID": "ford123"
    }]
};
$.each(a.Cars, function (key, value) {
    $("#dropDownDest").append($('<option></option>').val(value.carID).html(value.CarType));
});

$('#dropDownDest').change(function () {
    alert($(this).val());
});

// ------------------------------------------------------------------------------------------------------------
var cata = [];
var catagori = "";
var price = 0;
var price_list = {};

$(document).ready(function () {
    console.log("In ready");
    getcatagories();
});



var getcatagories = function () {
    $.getJSON("/bazaarapp/catagories", function (response) {
        data1 = "";
        var catagories_list = response.item_category;
        for (i = 0; i < catagories_list.length; i++) {
            var catagory = catagories_list[i];
            var data = $("#dropdown_cat").html()
                .replace("{data}", catagory)
                .replace("{catagory}", catagory);
            cata.push(catagory);
            data1 = data1 + data;
        }


        $(".catagory_datalist").append($(data1));
    });
};


$("#cat-form").submit(function (e) {
    e.preventDefault();
    cat = $("#cat-input-field").val();
    s = "/bazaarapp/item/";
    catagori = cat;
    document.getElementById("brand-form").action = s;
    getbrand(cat);
});


$("#brand-form").submit(function (e) {
    e.preventDefault();
    brand = $("#brand-input-field").val();
    document.getElementById("item-form").action = "nothing .asp";
    getitem(catagori, brand);
});

var item_name = "";
$("#item-form").submit(function (e) {
    e.preventDefault();
    item = $("#item-input-field").val();
    item_name = item;
    price = price_list[item];
    document.getElementById("amount").innerHTML = price;
});

no_of_Items = 1;
$(".number").focusout(function () {

    if ($(".number").val() >= 1) {
        no_of_Items = $(".number").val();
        price = price * no_of_Items;
        document.getElementById("amount").innerHTML = price;
    } else {
        document.getElementById("amount").innerHTML = price;
    }
});

var brand_name = "";

function getbrand(catagory) {
    $.getJSON("/bazaarapp/brands/" + catagory, function (response) {
        var brand_list = response.item_brand;
        var data = "";
        for (j = 0; j < brand_list.length; j++) {
            atag = $('#dropdown_brand').html()
                .replace("{data}", brand_list[j])
                .replace("{catagory}", catagory)
                .replace("{brand}", brand_list[j]);
            data += atag;
        }
        $('.brand_datalist').append(data);
    });
}

function getitem(c, b) {
    var x = 0;
    brand_name = b;
    if (b != null) {
        $.getJSON("/bazaarapp/item/" + c + "/" + b, function (response) {
            var item_list = Object.keys(response);
            for (i = 0; i < item_list.length; i++) {
                var item = item_list[i];
                var data = $("#dropdown_item").html()
                    .replace("{data}", item)
                    .replace("{item}", item);
                price_list = response;
                x = 1;
                $(".item_datalist").append($(data));
            }
        });
    }
    if (x == 1) {
        price = price_list[c];
    }
}

function add() {
    if ((catagori && brand_name && item_name && no_of_Items && price) != "") {
        insertTableRow(catagori, brand_name, item_name, no_of_Items, price);
        no_of_Items = 1;
        $(".brand").remove();
        $(".item").remove();
        $("#cat-input-field").val("");
        $("#brand-input-field").val("");
        $("#item-input-field").val("");
        $("#number-input-field").val("");
        document.getElementById("amount").innerHTML = 0.00
        console.log(transaction_data.list)
    }
}
var table_count = 0;
var transaction_data = {}
transaction_data.list = [];

function insertTableRow(cat, brand, itemname, no_of_items, amount) {
    table_contents = "";
    transaction_data.list[table_count] = [cat, brand, itemname, no_of_items, amount];
    // transaction_data.list[table_count] = [];
    // transaction_data.list[table_count].push(cat);
    // transaction_data.list[table_count].push(brand);
    // transaction_data.list[table_count].push(itemname);
    // transaction_data.list[table_count].push(no_of_items);
    // transaction_data.list[table_count].push(amount);

    console.log("len----"+transaction_data.list[table_count].length)
    table_count++;


    var data1 = $("#table_data").html()
        .replace("{data}", cat);
    var data2 = $("#table_data").html()
        .replace("{data}", brand);
    var data3 = $("#table_data").html()
        .replace("{data}", itemname);
    var data4 = $("#table_data").html()
        .replace("{data}", no_of_items);
    var data5 = $("#table_data").html()
        .replace("{data}", amount);
    console.log("but")
    but = "<td><button type=\"button\" class=\"btn btn-danger  button" + table_count +
        "\" onclick=\"close_row(" + table_count + ")\">X</button></td>";
    table_contents = data1 + data2 + data3 + data4 + data5 + but;

    row = "<tr class = \"close" + table_count + "\">" + table_contents + "</tr>";
    $(".tablebody").append($(row));
}

function close_row(num) {
    var class_name = ".close" + num;
    $(class_name).remove();
    var n = parseInt(num);
    n = n-1
    console.log(transaction_data);
    console.log(n);
    delete transaction_data.list[n];
    console.log(transaction_data);

    }
var transaction_id = null;
function get_bill_data() {

    console.log(transaction_data)
/*    $.getJSON("/bazaarapp/store/" ,transaction_data, function (response) {
        transaction_id = response.id;
    })
*/

    $.ajax({
        url: "/bazaarapp/store/",
        data: transaction_data,
        type: "POST",
        method: "POST",
    }).done(function(data) {
        generate_bill();
        // for (var i = 0 ; i <transaction_data.list.length; i++) {
        //     console.log(transaction_data.list[i]);
        
    });
}

var total=0;
function generate_bill(){


  for (var row in transaction_data.list) {
       var particulars = transaction_data.list[row][2];
       var qty = transaction_data.list[row][3];
       var price = transaction_data.list[row][4];    
      $(".billtable").append("<tr><td>"+particulars+"</td><td>"+qty+"</td><td>"+price+"</td><td>"+price+"</td></tr>");
      total = parseInt(price) + parseInt(total);

}      
  $(".billtable").append("<tr></tr><tr><td></td><td></td><td>Total</td><td>"+total+"</td></tr>");
  $('body').removeClass('modal-open');
      $('.modal-backdrop').remove();
      $("#close").modal("hide"); 
}
function printDiv(divName) 
{
     var printContents = document.getElementById(divName).innerHTML;
     var originalContents = document.body.innerHTML;
     
      
     document.body.innerHTML = printContents;

     window.print();
     window.location.reload();
    
     document.body.innerHTML = originalContents;
}
$("#close_bill").click(function(e){
<<<<<<< HEAD
   $("#myModal").close();
    
=======
    window.location.reload();
    $('#myModal').close();
>>>>>>> d75b7414be9ae89dec04e7f769ef802d655ba794
})

$(".reset").click(function(e){
        $(".brand").remove();
        $(".item").remove();
        $("#cat-input-field").val("");
        $("#brand-input-field").val("");
        $("#item-input-field").val("");
        $("#number-input-field").val("");
        document.getElementById("amount").innerHTML = 0.00

});

$(".cancel").click(function(e){
     window.location.reload();

});
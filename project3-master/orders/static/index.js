function hideAllItemTypes() {
    // Hides all the forms
    $("#pizza").hide();
    $("#pasta").hide();
    $("#sub").hide();
    $("#salad").hide();
    $("#dinner_platter").hide();
}

hideAllItemTypes();

$(function(){

    $("input[name=item_type]").change(function(){
        // The way the menu layout works is all the elements are rendered as hidden,
        // and then on the change of the radio button, it shows the relevant form
        hideAllItemTypes();
        switch(this.value) {
            case "pizza":
                $("#pizza").show(); break;
            case "pasta":
                $("#pasta").show(); break;
            case "sub":
                $("#sub").show(); break;
            case "salad":
                $("#salad").show(); break;
            case "dinner_platter":
                $("#dinner_platter").show();  break;
            default:
                console.log("invalid radion button");
        }
    });


    // Validation functions below.  They prevent then actions on 'Checkout' and 'Add to Cart' buttons
    // from running by disabling the button.  They check for things like 'kind' and 'size' being
    // selected to make sure the required fields are chosen.

    // Disabled checkout button if the cart is empty
    $("#checkout_button").prop('disabled', cart_size == 0);

    // Prevents more than five pizza toppings to be selected
    $(document).on("change", ".pizza_topping", function() {
        if($(".pizza_topping:checked").length >= 6) {
            this.checked = false;
        }
    });

    // Makes sure that all the required pizza fields are chosen
    $(document).on("change", ".pizza_kind", function() { form_validator_pizza() });
    $(document).on("change", ".pizza_size", function() { form_validator_pizza() });
    function form_validator_pizza() {
         $("#add_to_cart_pizza").prop('disabled', $(".pizza_kind:checked").length == 0 || $(".pizza_size:checked").length == 0);
    }

    // Makes sure that all the required sub fields are chosen
    $(document).on("change", ".sub_kind", function() { form_validator_sub() });
    $(document).on("change", ".sub_size", function() { form_validator_sub() });
    function form_validator_sub() {
         $("#add_to_cart_sub").prop('disabled', $(".sub_kind:checked").length == 0 || $(".sub_size:checked").length == 0);
    }

    // Makes sure that all the required pasta fields are chosen
    $(document).on("change", ".pasta_kind", function() { form_validator_pasta() });
    function form_validator_pasta() {
         $("#add_to_cart_pasta").prop('disabled', $(".pasta_kind:checked").length == 0);
    }

    // Makes sure that all the required salad fields are chosen
    $(document).on("change", ".salad_kind", function() { form_validator_salad() });
    function form_validator_salad() {
         $("#add_to_cart_salad").prop('disabled', $(".salad_kind:checked").length == 0);
    }

    // Makes sure that all the required dinner_platter fields are chosen
    $(document).on("change", ".dinner_platter_kind", function() { form_validator_dinner_platter() });
    $(document).on("change", ".dinner_platter_size", function() { form_validator_dinner_platter() });
    function form_validator_dinner_platter() {
         $("#add_to_cart_dinner_platter").prop('disabled', $(".dinner_platter_kind:checked").length == 0
                                                    || $(".dinner_platter_size:checked").length == 0);
    }

    // End Validation functions
});

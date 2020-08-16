$("#btn-1").click(function() {
    console.log("feg");
    $("#info").css("visibility", "hidden");
    $("#info").css("z-index", "-10");
    $("#form").css("visibility", "visible");
    $("#form").css("z-index", "10");
    $("#form").css("top", "-50%");
});

$("#btn-2").click(function() {
    console.log("sfdfdf");
    $(".container-fluid").load("info.html");
})
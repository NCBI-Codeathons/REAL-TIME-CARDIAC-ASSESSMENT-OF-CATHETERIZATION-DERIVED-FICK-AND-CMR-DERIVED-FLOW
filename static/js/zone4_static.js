$(document).ready(function(){
    setInterval(function() { 
      $.get('/get_live_data', function(response) { 
        $(".fra_qp").html(JSON.parse(response).fra_qp);
        $(".fra_qep").html(JSON.parse(response).fra_qep);
        $(".fra_qs").html(JSON.parse(response).fra_qs);
        $(".fra_qes").html(JSON.parse(response).fra_qes);
        $(".fra_qpqs").html(JSON.parse(response).fra_qpqs);
        $(".fra_qepqes").html(JSON.parse(response).fra_qepqes);
        $(".fra_qepqs").html(JSON.parse(response).fra_qepqs);
        $(".fra_pvr").html(JSON.parse(response).fra_pvr);
        $(".fra_svr").html(JSON.parse(response).fra_svr);
        $(".fra_rprs").html(JSON.parse(response).fra_rprs);
        $(".fno_qp").html(JSON.parse(response).fno_qp);
        $(".fno_qep").html(JSON.parse(response).fno_qep);
        $(".fno_qs").html(JSON.parse(response).fno_qs);
        $(".fno_qes").html(JSON.parse(response).fno_qes);
        $(".fno_qpqs").html(JSON.parse(response).fno_qpqs);
        $(".fno_qepqes").html(JSON.parse(response).fno_qepqes);
        $(".fno_qepqs").html(JSON.parse(response).fno_qepqs);
        $(".fno_pvr").html(JSON.parse(response).fno_pvr);
        $(".fno_svr").html(JSON.parse(response).fno_svr);
        $(".fno_rprs").html(JSON.parse(response).fno_rprs);
        $(".fl_qp").html(JSON.parse(response).fl_qp);
        $(".fl_qep").html(JSON.parse(response).fl_qep);
        $(".fl_qs").html(JSON.parse(response).fl_qs);
        $(".fl_qes").html(JSON.parse(response).fl_qes);
        $(".fl_qpqs").html(JSON.parse(response).fl_qpqs);
        $(".fl_qepqes").html(JSON.parse(response).fl_qepqes);
        $(".fl_qepqs").html(JSON.parse(response).fl_qepqs);
        $(".fl_pvr").html(JSON.parse(response).fl_pvr);
        $(".fl_svr").html(JSON.parse(response).fl_svr);
        $(".fl_rprs").html(JSON.parse(response).fl_rprs);
      }); 
    }, 4000); 
  });
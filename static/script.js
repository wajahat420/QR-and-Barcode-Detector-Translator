function showDetails(itemID){
  ids = ["h4-1","h4-2","h4-3","h4-5","h4-6","h4-7"]
  id = document.getElementById(itemID)

  // console.log("id",itemID)
    if (id.className == ""){
        id.className  = "d-none"
    }else{
      id.className  = ""
      for(i=0;i<ids.length;i++){
        otherId = document.getElementById(ids[i])
        if(itemID != ids[i]){
            otherId.className  = " d-none"
          }
      }
    }


  
}
var messages = [];

function  myFunction() {

  var text = $("#text").val();

  if( messages.length % 2 == 1){
    return
  }
  messages.push(text);
  id = document.getElementById("message")
  // console.log("text",text)
  document.getElementById("text").value = "";
  if (text == ""){
    return
  }
  var html = "<div class='right'>	<div>"  + text + " </div>	</div>";
  $(".message").append(html);
  id.scrollTop = id.scrollHeight ;

  // Speak Question
  $.ajax({
    url: "/textTospeech",
    type: "POST",
    data: { text: text }
    }).done((res) => {
        messages.push(res);
        // var html = "<div class='right'>	<div>"  + messages[messages.length - 1] + " </div>	</div>";
        // $(".message").append(html);
        var html = "<div class='left'>	<div>"  + res+ " </div>	</div>";
        $(".message").append(html);

        id.scrollTop = id.scrollHeight ;

        // for (i = messages.length - 2; i < messages.length; i++) {
        //     if (i % 2 == 1) {
        //       var html = "<div class='left'>	<div>"  + messages[i] + " </div>	</div>";
        //     } else {
        //       var html = "<div class='right'>	<div> " + messages[i] + " </div>	</div>";
        //     }
        //     $(".message").append(html);
        //     id.scrollTop = id.scrollHeight ;
        // }
        // Speak answer 
          // $.ajax({
          //   url: "/speak",
          //   type: "GET",
          // }).done((res)=>{
          //   console.log("no worries")
          // })
    });
}

function voiceRecord() {
  console.log("working...........")
  id = document.getElementById("message")

  $.ajax({
      url: "/speechToText",
      type: "GET"
  }).done((res) => {
  
    console.log("before")
      messages.push(res.ques);
      messages.push(res.ans);
      console.log("after")

      var html1 = "<div class='right'>	<div>" + res.ques + " </div>	</div>";
      $(".message").append(html1);
      var html2 = "<div class='left'>	<div> " + messages[messages.length - 1] + " </div>	</div>";
      $(".message").append(html2);

      id.scrollTop = id.scrollHeight;

  });
//   $.ajax({
//       url: "/speak",
//       type: "GET",
//   }).done((res) => {



//     id.scrollTop = id.scrollHeight;
//     // console.log("message", messages)

// });


}




